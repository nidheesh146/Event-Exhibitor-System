from rest_framework import serializers
from .models import Badge

class BadgeSerializer(serializers.ModelSerializer):
    ticket_name = serializers.CharField(source='ticket.name', read_only=True)

    class Meta:
        model = Badge
        fields = "__all__"

    def validate_email(self, value):

        instance = self.instance

        if Badge.objects.filter(email=value)\
            .exclude(id=getattr(instance, 'id', None))\
            .exists():
            raise serializers.ValidationError(
                "Email already exists"
            )

        return value
    
    
from rest_framework import serializers
from .models import Invitation

class InvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invitation
        fields = "__all__"

    def validate_email(self, value):

        if Invitation.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Invitation already sent"
            )

        return value
    
    
from rest_framework import serializers
from .models import UploadBatch, UploadRecord


class UploadBatchSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = UploadBatch
        fields = "__all__"


class UploadRecordSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = UploadRecord
        fields = "__all__"
        
        
        
        
from rest_framework import serializers

from .models import Invitation


class InvitationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Invitation

        fields = "__all__"

        read_only_fields = (
            "invitation_token",
            "is_used",
            "created_at",
            "status",
        )
        
        
from rest_framework import serializers

from .models import TicketType


class TicketTypeSerializer(serializers.ModelSerializer):

    class Meta:

        model = TicketType

        fields = (
            "id",
            "name",
        )
        
        
        
from rest_framework import serializers

from .models import Badge


class BadgeRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Badge
        fields = "__all__"

    def validate_terms_accepted(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must accept the Terms & Conditions."
            )
        return value
        




from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Exhibitor
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Exhibitor


class CreateExhibitorSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Exhibitor
        fields = [
            "username",
            "email",
            "password",
            "company_name",
            "contact_person",
            "phone_number",
            "allocated_badges",
        ]

    def create(self, validated_data):

        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "Username already exists."}
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists."}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        exhibitor = Exhibitor.objects.create(
            user=user,
            **validated_data
        )

        return exhibitor
    
    
    
    
    
from rest_framework import serializers
from .models import UploadBatch

class UploadBatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadBatch
        fields = [
            "id",
            "file_name",
            "uploaded_at"
        ]
        
        
        

from rest_framework import serializers
from .models import Exhibitor


class AllocateBadgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exhibitor
        fields = [
            "allocated_badges"
        ]
        
    
    

from rest_framework import serializers
from .models import Invitation


class InvitationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Invitation

        fields = [
            "first_name",
            "last_name",
            "email",
            "ticket"
        ]
        
        
class InvitationListSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    type = serializers.CharField(
        source="ticket.name",
        read_only=True
    )

    expiry = serializers.DateTimeField(
        source="expires_at",
        read_only=True
    )

    limit = serializers.IntegerField(
        source="link_limit",
        read_only=True
    )

    registered = serializers.IntegerField(
        source="registered_count",
        read_only=True
    )

    link = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = [
            "id",
            "name",
            "email",
            "type",
            "expiry",
            "limit",
            "registered",
            "status",
            "link"
        ]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_link(self, obj):

        request = self.context.get("request")

        return request.build_absolute_uri(
            f"/register/?token={obj.invitation_token}"
        )