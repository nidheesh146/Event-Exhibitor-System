from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import TicketType, Badge, UploadBatch, UploadRecord, Invitation, Exhibitor

class CreateBadgeTests(APITestCase):
    def setUp(self):
        self.ticket_type = TicketType.objects.create(name="VIP", allocated_count=10)

    def test_upload_records_list_filters_by_batch_and_paginates(self):
        batch_one = UploadBatch.objects.create(batch_name="Batch 1", file_name="batch1.xlsx")
        batch_two = UploadBatch.objects.create(batch_name="Batch 2", file_name="batch2.xlsx")

        UploadRecord.objects.create(batch=batch_one, row_data={"First Name": "Alice"}, is_valid=True)
        UploadRecord.objects.create(batch=batch_one, row_data={"First Name": "Bob"}, is_valid=False)
        UploadRecord.objects.create(batch=batch_two, row_data={"First Name": "Carol"}, is_valid=True)

        response = self.client.get(f"/upload-batch/{batch_one.id}/records/?page=1&page_size=1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertTrue(response.data["has_more"])

    def test_create_badge_success(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'job_title': 'Developer',
            'company_name': 'Test Corp',
            'phone_number': '+971501234567',
            'country_of_residence': 'United Arab Emirates',
            'nationality': 'Emirati',
            'ticket': self.ticket_type.id,
            'terms_accepted': True
        }
        response = self.client.post('/create-badge/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Badge.objects.count(), 1)
        badge = Badge.objects.first()
        self.assertEqual(badge.first_name, 'John')
        self.assertTrue(badge.terms_accepted)

    def test_create_badge_terms_rejected(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'job_title': 'Developer',
            'company_name': 'Test Corp',
            'phone_number': '+971501234567',
            'country_of_residence': 'United Arab Emirates',
            'nationality': 'Emirati',
            'ticket': self.ticket_type.id,
            'terms_accepted': False
        }
        response = self.client.post('/create-badge/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('terms_accepted', response.data)

    def test_send_invitation_attaches_invitation_to_logged_in_exhibitor(self):
        user = User.objects.create_user(username='exhibitor', password='secret123')
        exhibitor = Exhibitor.objects.create(user=user, company_name='Acme Ltd')

        self.client.force_authenticate(user=user)

        response = self.client.post('/send-invitation/', {
            'invitations': [{
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'jane@example.com',
                'ticket': self.ticket_type.id,
            }]
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        invitation = Invitation.objects.get(email='jane@example.com')
        self.assertEqual(invitation.exhibitor, exhibitor)

