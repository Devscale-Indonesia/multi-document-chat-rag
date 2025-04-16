from django.db import models
from core.models import BaseModel

class Conversation(BaseModel):
    role = models.CharField(max_length=255)
    message = models.TextField()
    document = models.ForeignKey("documents.Document", on_delete=models.SET_NULL, null=True)
