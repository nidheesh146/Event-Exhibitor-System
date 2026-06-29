from django.db import models
import uuid


class TicketType(models.Model):
    name = models.CharField(max_length=100)
    allocated_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    

class UploadBatch(models.Model):

    exhibitor = models.ForeignKey(
        'Exhibitor',
        on_delete=models.CASCADE,
        related_name='upload_batches',
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )
    batch_name = models.CharField(
        max_length=255
    )

    file_name = models.CharField(
        max_length=255
    )

    total_records = models.IntegerField(
        default=0
    )

    valid_records = models.IntegerField(
        default=0
    )
    status = models.CharField(
    max_length=20,
    default="processing"
    )

    invalid_records = models.IntegerField(
        default=0
    )
    def __str__(self):
        return self.file_name
    
    
    
    
from django.contrib.auth.models import User

class Exhibitor(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,null=True
    )

    company_name = models.CharField(max_length=200, unique=True)

    contact_person = models.CharField(max_length=100,  null=True, blank=True)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    allocated_badges = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.company_name
    
    
    

from django.db import models

class UploadRecord(models.Model):

    batch = models.ForeignKey(
        UploadBatch,
        on_delete=models.CASCADE,
        related_name="records"
    )

    row_data = models.JSONField()

    is_valid = models.BooleanField(
        default=False
    )

    error_message = models.TextField(
        blank=True,
        null=True
    )

    is_imported = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    
    
class ColumnMapping(models.Model):

    batch = models.ForeignKey(
        UploadBatch,
        on_delete=models.CASCADE
    )

    uploaded_column = models.CharField(
        max_length=255
    )

    system_field = models.CharField(
        max_length=255
    )
    
    
    




class Badge(models.Model):
    exhibitor = models.ForeignKey(
        Exhibitor,
        on_delete=models.CASCADE,null=True
    )
    STATUS_CHOICES = (
        ('invited', 'Invited'),
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
    )

    urn = models.UUIDField(default=uuid.uuid4, editable=False)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)

    phone_number = models.CharField(max_length=20)

    country_of_residence = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

    ticket = models.ForeignKey(
        TicketType,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    



class Invitation(models.Model):
    exhibitor = models.ForeignKey(
    Exhibitor,
    on_delete=models.CASCADE,
    related_name="invitations",
    null=True,
    blank=True
)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    ticket = models.ForeignKey(
        TicketType,
        on_delete=models.CASCADE
    )

    invitation_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("Invited", "Invited"),
            ("Confirmed", "Confirmed")
        ],
        default="Invited"
    )

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    link_limit = models.PositiveIntegerField(
        default=1
    )

    registered_count = models.PositiveIntegerField(
        default=0
    )
    
    
    
from django.db import models
import uuid


class Visitor(models.Model):

    invitation = models.OneToOneField(
        "Invitation",
        on_delete=models.CASCADE,
        related_name="visitor",
        null=True,
        blank=True
    )

    exhibitor = models.ForeignKey(
        "Exhibitor",
        on_delete=models.CASCADE,
        related_name="visitors"
    )

    ticket = models.ForeignKey(
        "TicketType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    company_name = models.CharField(
        max_length=255,
        blank=True
    )

    job_title = models.CharField(
        max_length=255,
        blank=True
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True
    )

    country_of_residence = models.CharField(
        max_length=100
    )

    nationality = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=30,
        choices=[
            ("Pending", "Pending"),
            ("Confirmed", "Confirmed"),
            ("Cancelled", "Cancelled")
        ],
        default="Confirmed"
    )

    badge_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"