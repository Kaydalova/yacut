import random
from datetime import datetime

from flask import url_for

from yacut import db
from .constants import (MAX_ORIGINAL_LENGTH, MAX_SHORT_LENGTH,
                        OUT_OF_SHORTS_MESSAGE, POPULATION_FOR_RANDOM_SHORT,
                        SHORT_LENGTH)
from .error_handlers import OutOfShortsException


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH))
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self, url_only=False):
        if url_only:
            return dict(url=self.original)
        return {
            'url': self.original,
            'short_link': url_for('index_view', _external=True) + self.short}

    @staticmethod
    def from_dict(data):
        """
        Функция создает экземпляр класса URLMap
        из переданного ей словаря data
        """
        urlmap = URLMap()
        model_fields_names = {
            'url': urlmap.__table__.columns[1].name,
            'custom_id': urlmap.__table__.columns[2].name}
        for field in ['url', 'custom_id']:
            if field in data:
                setattr(urlmap, model_fields_names[field], data[field])
        return urlmap

    @staticmethod
    def get_unique_short_id():
        """
        Функция генирирует уникальную короткую ссылку.
        Ссылка может состоять только из латинских букв
        и цифр от 0 до 9.
        """
        short = "".join(random.sample(POPULATION_FOR_RANDOM_SHORT, SHORT_LENGTH))
        if URLMap.get(short=short) is not None:
            raise OutOfShortsException(OUT_OF_SHORTS_MESSAGE)
        return short

    @classmethod
    def get(cls, **kwargs):
        return URLMap.query.filter_by(**kwargs).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
