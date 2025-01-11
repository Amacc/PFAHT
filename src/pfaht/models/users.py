from pydantic import BaseModel
from pypika import Field, Query, Table


class Users:
    table = Table("users")
    username: str = None
    """Username is an email and the primary key"""

    @classmethod
    def get_by_username(cls, username):
        q = Query.from_(cls.table).select("*").where(cls.table.username == username)
        return q.get_sql()

    @classmethod
    def create(cls, username, email):
        q = Query.into(cls.table).columns("username").insert(username)
        return q.get_sql()


class PageOptions(BaseModel):
    page: int = 1
    per_page: int = 100


class Notification:
    table = Table("notifications")
    notification_id: int = None
    """Notification ID is an autoincrementing integer and the primary key"""
    notification_message: str = None
    """System Notification Message"""
    enabled: bool = True

    @classmethod
    def list(cls, page_options: PageOptions):
        """List notifications"""
        q = (
            Query.from_(cls.table)
            .select("*")
            .limit(page_options.per_page)
            .offset((page_options.page - 1) * page_options.per_page)
        )
        return q.get_sql()

    @classmethod
    def create(cls, notification_message):
        q = (
            Query.into(cls.table)
            .columns("notification_message")
            .insert(notification_message)
        )
        return q.get_sql()

    @classmethod
    def disable(cls, notification_id):
        q = (
            Query.update(cls.table)
            .set("enabled", False)
            .where(cls.table.notification_id == notification_id)
        )
        return q.get_sql()


class UserViewedNotification(BaseModel):
    table = Table("acknowledged_notifications")
    viewed_username: str = Field(alias="username")
    """The username who viewed the notification"""
    notification_id: int = None
    """The notification ID that was viewed"""

    @classmethod
    def create(cls, viewed_username, notification_id):
        q = (
            Query.into(cls.table)
            .columns("viewed_username", "notification_id")
            .insert(viewed_username, notification_id)
        )
        return q.get_sql()

    @classmethod
    def list(cls, username):
        q = (
            Query.from_(cls.table)
            .select("*")
            .where(cls.table.viewed_username == username)
        )
        return q.get_sql()
