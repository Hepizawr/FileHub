import typing as t
import uuid

from app import db


class File(db.Model):
    __tablename__ = "file"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), unique=True, nullable=False)
    format = db.Column(db.String(50), nullable=True)

    _users = db.relationship(
        "User",
        secondary="permission",
        back_populates="_files",
    )
    downloads = db.relationship(
        "Download",
        foreign_keys="Download.file_id",
        back_populates="file",
        cascade="all, delete",
    )

    @property
    def users(self):
        return self._users

    @users.setter
    def users(self, usernames: t.List[str]):
        from app.models import User

        self._users = [user for username in usernames if (user := User.query.filter_by(username=username).first())]

    @property
    def download_count(self):
        return len(self.downloads)

    @property
    def filename(self):
        return str(self.id) + self.format
