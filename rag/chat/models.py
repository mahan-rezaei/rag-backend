from django.db import models


class Document(models.Model):
    file_name = models.CharField(max_length=300)
    is_proccessed = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    