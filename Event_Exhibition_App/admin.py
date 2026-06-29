from django.contrib import admin
from .models import Badge, TicketType, Invitation,Visitor, ColumnMapping, UploadBatch, UploadRecord

admin.site.register(Badge)
admin.site.register(TicketType)
admin.site.register(Invitation)
admin.site.register(UploadBatch)
admin.site.register(UploadRecord)
admin.site.register(ColumnMapping)
admin.site.register(Visitor)



from django.contrib import admin
from .models import Exhibitor

@admin.register(Exhibitor)
class ExhibitorAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "contact_person",
        "phone_number",
        "allocated_badges",
        "user"
    )

    search_fields = (
        "company_name",
        "contact_person"
    )

    list_filter = (
        "allocated_badges",
    )