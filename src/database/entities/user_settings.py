from mongoengine import Document, IntField, StringField


class UserSettings(Document):
    user_id = IntField(required=True, primary_key=True)
    language_code = StringField(required=True)

    meta = {'collection': 'user_settings'}
