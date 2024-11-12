from .. import db


class UserFile(db.Model):
    __tablename__ = 'user_files'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id', ondelete="CASCADE"), primary_key=True)
