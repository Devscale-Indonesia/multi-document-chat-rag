from django.db import models

from core.models import BaseModel

DOC_PROCESS_PENDING = "pending"
DOC_PROCESS_PROCESSING = "processing"
DOC_PROCESS_DONE = "done"

DOC_PROCESS_STATUS = (
    (DOC_PROCESS_PENDING, "Pending"),
    (DOC_PROCESS_PROCESSING, "Processing"),
    (DOC_PROCESS_DONE, "Done"),
)


class Document(BaseModel):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    status = models.CharField(
        max_length=255, default=DOC_PROCESS_PENDING, choices=DOC_PROCESS_STATUS
    )
    raw_text = models.TextField(blank=True, null=True)
    summary_text = models.TextField(blank=True, null=True)
