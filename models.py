from pymodm import fields, MongoModel


class User(MongoModel):
    email = fields.email(primary_key = True)
    picture = fields.LineStringField()
    process_duration = fields.ListFields()
    upload_time = fields.ListFields()
    image_size = fields.ListFields() # Tupel
    pass
