from .. import db
from datetime import datetime


class Download(db.Model):
    __tablename__ = 'downloads'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id', ondelete="CASCADE"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='downloads')
    file = db.relationship('File', back_populates='downloads')
