from .download import Download
from .file import File
from .permission import Permission
from .user import User

__all__ = ["User", "File", "Permission", "Download"]

import sqlalchemy as sql
import sqlalchemy.event as event

# @event.listens_for(target=File, identifier="after_insert")
# def create_download_counter(mapper, connection, target):
#     stmt = sql.insert(DownloadTotalCount).values(file_id=target.id)
#     connection.execute(stmt)
#
#
# @event.listens_for(target=Download, identifier="after_insert")
# def increment_download_counter(mapper, connection, target):
#     stmt = (
#         sql.update(DownloadTotalCount)
#         .where(file_id=target.file_id)
#         .values(count=DownloadTotalCount.count + 1)
#     )
#     connection.execute(stmt)
