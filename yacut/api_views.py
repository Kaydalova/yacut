import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (EMPTY_BODY_MESSAGE, ID_NOT_FOUND_MESSAGE,
                        INVALID_CUSTOM_ID_MESSAGE, INVALID_URL_MESSAGE,
                        NO_URL_MESSAGE, NOT_UNIQUE_CUSTOM_ID_MESSAGE,
                        REGEX_FOR_ORIGINAL_URL, REGEX_FOR_SHORL_URL)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


def validate_attributes(data):
    """
    Функция проверяет атрибуты запроса:
    - наличие url и его корректность
    - если указан custom_id проверяет его уникальность,
    соответствие регулярному выражению. Если не указан формирует его.
    """

    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL_MESSAGE)

    if not re.match(REGEX_FOR_ORIGINAL_URL, data['url']):
        raise InvalidAPIUsage(
            INVALID_URL_MESSAGE,
            HTTPStatus.BAD_REQUEST)

    if 'custom_id' in data:
        short = data.get('custom_id')
        if URLMap.get(short=short):
            raise InvalidAPIUsage(
                NOT_UNIQUE_CUSTOM_ID_MESSAGE.format(custom_id=short),
                HTTPStatus.BAD_REQUEST)
        if not short or short == "":
            data['custom_id'] = URLMap.get_unique_short_id()
        elif not re.match(REGEX_FOR_SHORL_URL, short):
            raise InvalidAPIUsage(
                INVALID_CUSTOM_ID_MESSAGE,
                HTTPStatus.BAD_REQUEST)
    else:
        data['custom_id'] = URLMap.get_unique_short_id()
    return data


@app.route('/api/id/', methods=['POST'])
def get_short():
    """
    Обработка запроса на создание новой короткой ссылки.
    """
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_BODY_MESSAGE)
    data = validate_attributes(data)
    urlmap = URLMap.from_dict(data)
    urlmap.save()
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    """
    Получение оригинальной ссылки по короткому идентификатору.
    """
    original_url = URLMap.get(short=short_id)
    if original_url is None:
        raise InvalidAPIUsage(
            ID_NOT_FOUND_MESSAGE,
            HTTPStatus.NOT_FOUND)
    return jsonify(original_url.to_dict(url_only=True)), HTTPStatus.OK
