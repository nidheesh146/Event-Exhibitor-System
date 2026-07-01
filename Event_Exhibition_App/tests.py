from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import TicketType, Badge, UploadBatch, UploadRecord, Invitation, Exhibitor

class CreateBadgeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='exhibitor', password='secret123')
        self.exhibitor = Exhibitor.objects.create(user=self.user, company_name='Acme Ltd', allocated_badges=10)
        self.ticket_type = TicketType.objects.create(name="VIP", allocated_count=10)
        self.client.force_authenticate(user=self.user)

    def test_upload_records_list_filters_by_batch_and_paginates(self):
        # batch_one belongs to self.exhibitor
        batch_one = UploadBatch.objects.create(batch_name="Batch 1", file_name="batch1.xlsx", exhibitor=self.exhibitor)
        
        # batch_two belongs to a different exhibitor
        other_user = User.objects.create_user(username='other_exhibitor', password='secret123')
        other_exhibitor = Exhibitor.objects.create(user=other_user, company_name='Other Ltd', allocated_badges=10)
        batch_two = UploadBatch.objects.create(batch_name="Batch 2", file_name="batch2.xlsx", exhibitor=other_exhibitor)

        UploadRecord.objects.create(batch=batch_one, row_data={"First Name": "Alice"}, is_valid=True)
        UploadRecord.objects.create(batch=batch_one, row_data={"First Name": "Bob"}, is_valid=False)
        UploadRecord.objects.create(batch=batch_two, row_data={"First Name": "Carol"}, is_valid=True)

        response = self.client.get("/upload-records/?page=1&page_size=1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # It should only return records for self.exhibitor's batches (batch_one has 2 records)
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
        self.assertEqual(invitation.exhibitor, self.exhibitor)

    def test_process_upload_batch_robustness(self):
        from .views import process_upload_batch
        
        # Test CSV upload processing robustness
        csv_content = b"First Name,Last Name,Email,Phone,Job Title,Company\nAlice,Smith,alice@example.com,1234567890,Manager,Acme Corp\nBob,Jones,123456,9876543210,Developer,Beta Corp"
        batch = UploadBatch.objects.create(batch_name="CSV Batch", file_name="test.csv", exhibitor=self.exhibitor)
        
        process_upload_batch(batch.id, "test.csv", csv_content)
        
        batch.refresh_from_db()
        self.assertEqual(batch.status, "completed")
        self.assertEqual(batch.total_records, 2)
        
        records = batch.records.all()
        self.assertEqual(records.count(), 2)
        
        # Verify Alice is valid
        alice_rec = next(r for r in records if r.row_data.get("First Name") == "Alice")
        self.assertTrue(alice_rec.is_valid)
        self.assertEqual(alice_rec.row_data.get("Email"), "alice@example.com")
        
        # Verify Bob is invalid because of bad email format, but didn't crash
        bob_rec = next(r for r in records if r.row_data.get("First Name") == "Bob")
        self.assertFalse(bob_rec.is_valid)
        self.assertIn("Invalid email format", bob_rec.error_message)

    def test_bulk_delete_wipes_badges_and_uploads(self):
        # Create a batch and an upload record for the exhibitor
        batch = UploadBatch.objects.create(batch_name="Batch 1", file_name="batch1.xlsx", exhibitor=self.exhibitor)
        UploadRecord.objects.create(batch=batch, row_data={"First Name": "Alice"}, is_valid=True)
        
        # Create a badge for the exhibitor
        Badge.objects.create(
            exhibitor=self.exhibitor,
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            job_title="Manager",
            company_name="Acme Corp",
            phone_number="1234567890",
            country_of_residence="UAE",
            nationality="Emirati",
            ticket=self.ticket_type,
            status="confirmed"
        )
        
        self.assertEqual(UploadRecord.objects.filter(batch__exhibitor=self.exhibitor).count(), 1)
        self.assertEqual(Badge.objects.filter(exhibitor=self.exhibitor).count(), 1)
        
        # Call the bulk delete API
        response = self.client.delete("/upload-records/bulk-delete/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify both UploadRecords and Badges are wiped
        self.assertEqual(UploadRecord.objects.filter(batch__exhibitor=self.exhibitor).count(), 0)
        self.assertEqual(Badge.objects.filter(exhibitor=self.exhibitor).count(), 0)

    def test_bulk_delete_badges_ownership_security(self):
        # Create a badge for the exhibitor
        badge = Badge.objects.create(
            exhibitor=self.exhibitor,
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            job_title="Manager",
            company_name="Acme Corp",
            phone_number="1234567890",
            country_of_residence="UAE",
            nationality="Emirati",
            ticket=self.ticket_type,
            status="confirmed"
        )
        
        # Create another exhibitor and badge
        other_user = User.objects.create_user(username='other_exhibitor2', password='secret123')
        other_exhibitor = Exhibitor.objects.create(user=other_user, company_name='Other Ltd 2', allocated_badges=10)
        other_badge = Badge.objects.create(
            exhibitor=other_exhibitor,
            first_name="Bob",
            last_name="Jones",
            email="bob@example.com",
            job_title="Developer",
            company_name="Other Corp",
            phone_number="9876543210",
            country_of_residence="UAE",
            nationality="Emirati",
            ticket=self.ticket_type,
            status="confirmed"
        )
        
        # Call the bulk delete badge API trying to delete both IDs, but only self.exhibitor's badge should be deleted
        response = self.client.post("/badges/bulk-delete/", {"ids": [badge.id, other_badge.id]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # badge should be deleted, other_badge should NOT be deleted
        self.assertFalse(Badge.objects.filter(id=badge.id).exists())
        self.assertTrue(Badge.objects.filter(id=other_badge.id).exists())

    def test_export_badges_contains_both_badges_and_uploads(self):
        # Create a badge
        Badge.objects.create(
            exhibitor=self.exhibitor,
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            job_title="Manager",
            company_name="Acme Corp",
            phone_number="1234567890",
            country_of_residence="UAE",
            nationality="Emirati",
            ticket=self.ticket_type,
            status="confirmed"
        )
        # Create a batch and an upload record
        batch = UploadBatch.objects.create(batch_name="Batch 1", file_name="batch1.xlsx", exhibitor=self.exhibitor)
        UploadRecord.objects.create(
            batch=batch,
            row_data={
                "First Name": "Bob",
                "Last Name": "Jones",
                "Company": "Beta Corp",
                "Job Title": "Developer",
                "Ticket": "VIP",
                "Phone": "9876543210",
                "Email": "bob@example.com"
            },
            is_valid=True
        )

        response = self.client.get("/badges/export/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.assertIn("attachment; filename=", response["Content-Disposition"])

        # Parse response with openpyxl to check content
        from io import BytesIO
        from openpyxl import load_workbook
        wb = load_workbook(BytesIO(response.getvalue()))
        sheet = wb.active
        self.assertEqual(sheet.title, "All Records")

        rows = list(sheet.values)
        self.assertEqual(rows[0], ("Name", "Company Name", "Job Title", "Ticket Name", "Status", "Phone", "Email", "Source", "Created At"))
        
        # Verify Alice (Badge) is in the output
        alice_row = next(r for r in rows if r[0] == "Alice Smith")
        self.assertEqual(alice_row[1], "Acme Corp")
        self.assertEqual(alice_row[6], "alice@example.com")
        self.assertEqual(alice_row[7], "Badge")

        # Verify Bob (UploadRecord) is in the output
        bob_row = next(r for r in rows if r[0] == "Bob Jones")
        self.assertEqual(bob_row[1], "Beta Corp")
        self.assertEqual(bob_row[6], "bob@example.com")
        self.assertEqual(bob_row[7], "Bulk Upload")

