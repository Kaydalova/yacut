import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import (REGEX_FOR_SHORL_URL, EMPTY_BODY_MESSAGE,
                        NO_URL_MESSAGE, INVALID_CUSTOM_ID_MESSAGE,
                        NOT_UNIQUE_CUSTOM_ID_MESSAGE, ID_NOT_FOUND_MESSAGE)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import check_unique_url, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def get_short():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_BODY_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL_MESSAGE)
    if 'custom_id' in data:
        short = data.get('custom_id')
        if not check_unique_url(short):
            raise InvalidAPIUsage(
                NOT_UNIQUE_CUSTOM_ID_MESSAGE.format(custom_id=short),
                HTTPStatus.BAD_REQUEST)
        if short is None or short == "":
            data['custom_id'] = get_unique_short_id()
        elif not re.match(REGEX_FOR_SHORL_URL, short):
            raise InvalidAPIUsage(
                INVALID_CUSTOM_ID_MESSAGE,
                HTTPStatus.BAD_REQUEST)
    else:
        data['custom_id'] = get_unique_short_id()
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.url_and_short_to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    original_url = URLMap.query.filter_by(short=short_id).first()
    if original_url is None:
        raise InvalidAPIUsage(
            ID_NOT_FOUND_MESSAGE,
            HTTPStatus.NOT_FOUND)
    return jsonify(original_url.url_to_dict()), HTTPStatus.OK
