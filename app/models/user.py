import typing as t
import uuid

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    _files = db.relationship(
        "File",
        secondary="permission",
        back_populates="_users",
    )
    downloads = db.relationship("Download", foreign_keys="Download.user_id", back_populates="user")

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, files: t.List["File"]):
        self._files = files

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
