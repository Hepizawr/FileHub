import os
import re
import traceback

from .. import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    format = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(255), nullable=False)

    users = db.relationship('User', secondary='user_files', back_populates='files')
    downloads = db.relationship('Download', back_populates='file', cascade='all, delete')

    @property
    def download_count(self):
        return len(self.downloads)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'format': self.format,
            'url': self.url,
            'users': [user.to_dict() for user in self.users],
            # 'downloads': self.downloads.to_dict(),
        }
