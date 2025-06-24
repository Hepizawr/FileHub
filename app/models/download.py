import datetime as dt
import uuid

from app import db


class Download(db.Model):
    __tablename__ = "download"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    file_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("file.id", ondelete="CASCADE"),
        nullable=False,
    )
    timestamp = db.Column(db.DateTime, default=dt.datetime.utcnow)

    user = db.relationship("User", back_populates="downloads")
    file = db.relationship("File", back_populates="downloads")
