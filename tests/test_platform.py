"""
NAGARAM — Comprehensive Automated Test Suite
Tests authentication, role routing, dashboards, and API endpoints.
"""
import unittest
from app import create_app
from app.extensions import db
from app.models.user import User, Role
from app.models.issue import Issue, IssueCategory
from app.models.scheme import GovernmentScheme


class NagaramTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_landing_page(self):
        """Test landing page renders with 200 OK."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'NAGARAM', response.data)

    def test_login_page(self):
        """Test login page renders with 200 OK."""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)

    def test_registration_page(self):
        """Test registration page renders with 200 OK."""
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)

    def test_demo_user_logins(self):
        """Test login flow for all demo user roles."""
        demo_accounts = [
            ('admin@nagaram.gov.in', '/admin/dashboard'),
            ('citizen@nagaram.gov.in', '/citizen/dashboard'),
            ('farmer@nagaram.gov.in', '/farmer/dashboard'),
            ('expert@nagaram.gov.in', '/expert/dashboard'),
            ('ngo@nagaram.gov.in', '/ngo/dashboard'),
            ('volunteer@nagaram.gov.in', '/volunteer/dashboard'),
        ]

        for email, expected_dashboard in demo_accounts:
            response = self.client.post('/auth/login', data={
                'login': email,
                'password': 'demo123',
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200, f"Failed login for {email}")
            self.assertIn(expected_dashboard.encode(), response.request.path.encode(), f"Dashboard mismatch for {email}")

    def test_farmer_modules(self):
        """Test all 15+ farmer module endpoints render OK."""
        # Login as farmer
        self.client.post('/auth/login', data={'login': 'farmer@nagaram.gov.in', 'password': 'demo123'})

        farmer_urls = [
            '/farmer/dashboard',
            '/farmer/weather',
            '/farmer/water-advisory',
            '/farmer/crop-health',
            '/farmer/market',
            '/farmer/advisor',
            '/farmer/soil',
            '/farmer/crop-recommendation',
            '/farmer/post-harvest',
            '/farmer/transport',
            '/farmer/schemes',
            '/farmer/farm-records',
            '/farmer/marketplace',
            '/farmer/buyer-connection',
            '/farmer/report-issue',
            '/farmer/notifications',
            '/farmer/profile',
        ]

        for url in farmer_urls:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed GET for {url}")


if __name__ == '__main__':
    unittest.main()
