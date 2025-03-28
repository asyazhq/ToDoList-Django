from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import UserModel, TodoListModel

class APITestCaseEndpoints(APITestCase):
    
    def setUp(self):
        # Create a test user
        self.user = UserModel.objects.create_user(username='testuser', password='password123', first_name='Test')
        self.client.force_authenticate(user=self.user)
        
        # Create another test user (for permission tests)
        self.other_user = UserModel.objects.create_user(username='otheruser', password='password123', first_name='Other')
        
        # Create a test task
        self.task = TodoListModel.objects.create(
            title='Test Task', description='Task description', status='new', owner=self.user
        )
        
        # Define URLs for endpoints
        self.task_url = reverse('task-detail', kwargs={'pk': self.task.id})
        self.mark_completed_url = reverse('task-mark-completed', kwargs={'pk': self.task.id})
        self.user_tasks_url = reverse('user-tasks')
        self.user_list_url = reverse('user-list')
        self.user_detail_url = reverse('user-detail', kwargs={'pk': self.user.id})

    def test_user_registration(self):
        """
        Test user registration.
        """
        data = {'username': 'newuser', 'password': 'password123', 'first_name': 'New'}
        response = self.client.post(self.user_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_user_tasks(self):
        response = self.client.get(self.user_tasks_url)
        print("Response data:", response.data)  

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        self.assertTrue(all(task['owner'] == self.user.username for task in response.data["results"]),
                    "Non-owned tasks included in response")
    
        self.assertEqual(response.data["count"], 1)  # Should only return this user's tasks

    def test_create_task(self):
        """
        Test task creation.
        """
        data = {'title': 'New Task', 'description': 'New task description', 'status': 'new'}
        response = self.client.post(self.user_tasks_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TodoListModel.objects.filter(title="New Task").exists())

    def test_retrieve_task(self):
        """
        Test retrieving a task.
        """
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_update_task(self):
        """
        Test updating a task.
        """
        data = {'title': 'Updated Task', 'description': 'Updated description', 'status': 'in_progress'}
        response = self.client.put(self.task_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'in_progress')

    def test_delete_task(self):
        """
        Test deleting a task.
        """
        response = self.client.delete(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TodoListModel.objects.filter(id=self.task.id).exists())

    def test_mark_task_completed(self):
        """
        Test marking a task as completed.
        """
        response = self.client.patch(self.mark_completed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'completed')

    def test_other_user_cannot_modify_task(self):
        self.client.force_authenticate(user=self.other_user)

        task_url = reverse('task-detail', kwargs={'pk': self.task.id})

        response = self.client.put(task_url, {'title': 'Unauthorized Update'})

        print("Modify Task Response:", response.status_code)  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_other_user_cannot_delete_task(self):
        self.client.force_authenticate(user=self.other_user)

        task_url = reverse('task-detail', kwargs={'pk': self.task.id})

        response = self.client.delete(task_url)

        print("Delete Task Response:", response.status_code)  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_retrieve_non_existent_task(self):
        """
        Test retrieving a non-existent task returns 404.
        """
        invalid_url = reverse('task-detail', kwargs={'pk': 99999})  # Non-existent task ID
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
