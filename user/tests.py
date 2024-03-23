# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser

class CustomUserTests(APITestCase):

    def setUp(self):
        # Create a user instance for testing
        CustomUser.objects.create(name="John Doe", description="A test user")

    def test_list_users(self):
        """
        Ensure we can list users.
        """
        url = reverse('customuser-list')  # Use the name of your user list route
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming this is the first user

    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('customuser-list')  # Use the name of your user list route
        data = {'name': 'Jane Doe', 'description': 'Another test user'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  # Including the user created in setUp

    def test_retrieve_user(self):
        """
        Ensure we can retrieve a user by id.
        """
        user = CustomUser.objects.get(name="John Doe")
        url = reverse('customuser-detail', kwargs={'pk': user.pk})  # Use the name of your user detail route
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], user.name)

    def test_update_user(self):
        """
        Ensure we can update an existing user.
        """
        user = CustomUser.objects.get(name="John Doe")
        url = reverse('customuser-detail', kwargs={'pk': user.pk})
        updated_data = {'name': 'John Updated', 'description': user.description}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.name, 'John Updated')

    def test_delete_user(self):
        """
        Ensure we can delete a user.
        """
        user = CustomUser.objects.get(name="John Doe")
        url = reverse('customuser-detail', kwargs={'pk': user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 0)
