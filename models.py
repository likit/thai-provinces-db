from mongoengine import *


class Area(Document):
    aid = IntField()
    level = StringField()  # "ch": province, "ta": Subdistrict, "am": District
    th_name = StringField()
    en_name = StringField()
    latlng = PointField()
    parent = ReferenceField("self", reverse_delete_rule=CASCADE)
    childs = ListField(ReferenceField("self"), default=[])
