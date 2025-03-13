from django.test import TestCase, Client
import json

class EmailGenerationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_generate_email(self):
        response = self.client.post(
            "/email/generate/",
            json.dumps({
                "from": "admin@company.com",
                "to": "user@example.com",
                "subject": "Password Reset Request"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.json())
