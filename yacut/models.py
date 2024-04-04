from datetime import datetime

from . import db


class URLMap(db.Model):
    """Модель проекта."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(255))
    short = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': f'http://localhost/{self.short}',
        }

    def from_dict(self, data):
        attribute = {'url': 'original', 'custom_id': 'short'}
        for key, attr in attribute.items():
            setattr(self, attr, data.get(key))
