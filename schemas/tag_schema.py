from extensions import ma
from models.tag import Tag


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True  # deserialize straight back into a Tag object


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)  # For serializing multiple tags
