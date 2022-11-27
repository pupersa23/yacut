from datetime import datetime

from flask import url_for

from . import db

LIMIT = 16


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(LIMIT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', custom_id=self.short, _external=True)
        )

    def to_short_dict(self):
        return dict(
            url=self.original
        )

    def from_dict(self, data):
        fields = {
            'url': 'original',
            'custom_id': 'short'
        }
        for field in fields:
            if field in data:
                setattr(self, field, data[field])
