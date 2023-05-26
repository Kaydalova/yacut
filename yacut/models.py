from datetime import datetime

from flask import url_for

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256))
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def url_to_dict(self):
        return dict(
            url=self.original)

    def url_and_short_to_dict(self):
        return {'url': self.original,
                'short_link': url_for('index_view', _external=True) + self.short}

    def from_dict(self, data):
        model_fields_names = {
            'url': 'original',
            'custom_id': 'short'}
        for field in ['url', 'custom_id']:
            if field in data:
                setattr(self, model_fields_names[field], data[field])
