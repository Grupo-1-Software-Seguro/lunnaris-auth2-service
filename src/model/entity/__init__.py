from mongoengine import Document, StringField


class UserAuth(Document):
    userId = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)