import uuid

from app import db


class Permission(db.Model):
    __tablename__ = "permission"

    user_id = db.Column(db.UUID, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    file_id = db.Column(db.UUID, db.ForeignKey("file.id", ondelete="CASCADE"), primary_key=True)
