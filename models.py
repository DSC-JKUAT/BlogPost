import re
from datetime import datetime


class Blog:
    blog_id = 1

    def __init__(self, title=None, content=None):
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.id = Blog.blog_id

        Blog.blog_id += 1


class Validators:

    @classmethod
    def valid_title(cls, title):
        return re.match("^[a-zA-Z0-9 ]{3,20}$", title)

    @classmethod
    def valid_content(cls, content):
        return re.match("^[a-zA-Z0-9,$&\.+*/' ]{10,}$", content)
