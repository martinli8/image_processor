from pymodm import fields, MongoModel


class User(MongoModel):
    email = fields.EmailField(primary_key=True)
    picture = fields.ListField()
    process_requested = fields.ListField()
    upload_time = fields.ListField(field=fields.DateTimeField())
    image_size = fields.ListField()
    process_duration = fields.ListField(blank=True)
    processed_image_fp = fields.ListField(blank=True)
    pass
