from marshmallow import Schema, fields

from app import db
from models import User


class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    movie_id = fields.Int(dump_only=True)
    rating = fields.Int(dump_only=True)
    comments = fields.Str(allow_none=True)
    date =  fields.Date(allow_none=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    reviews = fields.List(
        fields.Nested(
            "ReviewSchema",
            exclude=("user_id",)
        ),
        dump_only=True
    )

    