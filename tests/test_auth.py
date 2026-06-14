import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestRegistration:
    def test_register_page_loads(self, client):
        url = reverse('users:register')
        response = client.get(url)
        assert response.status_code == 200

    def test_register_with_valid_data(self, client, db):
        url = reverse('users:register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'strongpass123!',
            'password2': 'strongpass123!',
        }
        response = client.post(url, data)

        assert response.status_code == 302
        assert User.objects.filter(username='newuser').exists()

    def test_register_with_mismatched_passwords(self, client, db):
        url = reverse('users:register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'strongpass123!',
            'password2': 'differentpass!',
        }
        response = client.post(url, data)

        assert response.status_code == 200
        assert not User.objects.filter(username='newuser').exists()

    def test_register_with_existing_username(self, client, user):
        url = reverse('users:register')
        data = {
            'username': 'testuser',
            'email': 'new@example.com',
            'password1': 'strongpass123!',
            'password2': 'strongpass123!',
        }
        response = client.post(url, data)
        assert response.status_code == 200


@pytest.mark.django_db
class TestLogin:
    def test_login_page_loads(self, client):
        url = reverse('users:login')
        response = client.get(url)
        assert response.status_code == 200

    def test_login_with_valid_credentials(self, client, user):
        url = reverse('users:login')
        response = client.post(url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code == 302

    def test_login_with_wrong_password(self, client, user):
        url = reverse('users:login')
        response = client.post(url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        assert response.status_code == 200

    def test_logout(self, authenticated_client):
        url = reverse('users:logout')
        response = authenticated_client.post(url)
        assert response.status_code == 302
