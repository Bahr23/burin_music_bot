from tortoise.models import Model
from tortoise import fields


class User(Model):
    class Meta:
        table = 'users'
        ordering = ['created_at']
        
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    status = fields.CharField(max_length=10, default='user')
    username = fields.CharField(max_length=64, null=True)
    first_name = fields.CharField(max_length=64, null=True)
    last_name = fields.CharField(max_length=64, null=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    language_code = fields.CharField(max_length=8, null=True)
    
    likns: fields.ReverseRelation['Link']
    

class Post(Model):
    class Meta:
        table = 'static_content'

    id = fields.BigIntField(pk=True)
    tag = fields.CharField(max_length=64)
    text = fields.TextField(null=True)
    description = fields.CharField(max_length=256, null=True)
    photo_file_id = fields.CharField(max_length=256, null=True)
    video_file_id = fields.CharField(max_length=256, null=True)
    video_note_id = fields.CharField(max_length=256, null=True)
    audio_file_id = fields.CharField(max_length=256, null=True)
    document_file_id = fields.CharField(max_length=256, null=True)
    sticker_file_id = fields.CharField(max_length=256, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    
class Link(Model):
    class Meta:
        table = 'links'
        
    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='links')
    url = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
