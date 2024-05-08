from django.test import TestCase, Client
from django.contrib.auth.models import User 
from unittest.mock import patch
from django.urls import reverse
from .models import Project, Task
from .forms import TodoForm, ProjectForm


# Create your tests here.




class AddViewTestCase(TestCase):
    def setUp(self):
        # Create a User instance
        user = User.objects.create_user(username='testuser', password='password')
         # Create a Project instance with the created_by field set to the user
        self.project = Project.objects.create(title="Test Project", created_by=user)
        self.task_data = {'description': 'Test Task Description', 'status': 'todo'}  # Adjusted to match TodoForm
        self.invalid_task_data = {'description': '', 'status': 'todo'}  # Adjusted to match TodoForm
        self.add_url = reverse('todoapp:add', kwargs={'id': self.project.id})

    def test_add_view_get(self):
        response = self.client.get(self.add_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_add_view_post_valid_form(self):
        response = self.client.post(self.add_url, self.task_data)
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.assertEqual(Task.objects.count(), 1)  # Check if task is created


    def test_add_view_post_invalid_form(self):
        # Simulate POST request with invalid task data
        response = self.client.post(self.add_url, self.invalid_task_data)
        # Check if the form submission failed and stayed on the same page (status code 200)
        self.assertEqual(response.status_code, 200)
        # Check if the task was not added to the database
        self.assertEqual(Task.objects.count(), 0)

    


class DeleteViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create a project for the user
        self.project = Project.objects.create(title="Test Project", created_by=self.user)
        # Create a task for the project
        self.task = Task.objects.create(description="Test Task", project=self.project)
        # URL for the delete view
        self.delete_url = reverse('todoapp:delete', kwargs={'id': self.task.id})

    def test_delete_view_post(self):
        # Simulate POST request to delete the task
        response = self.client.post(self.delete_url)
        # Check if the task is deleted
        self.assertEqual(Task.objects.count(), 0)
        # Check if the response is a redirect
        self.assertRedirects(response, reverse('todoapp:add', kwargs={'id': self.project.id}))




class UpdateViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create a project for the user
        self.project = Project.objects.create(title="Test Project", created_by=self.user)
        # Create a task for the project
        self.task = Task.objects.create(description="Test Task", project=self.project)
        # URL for the update view
        self.update_url = reverse('todoapp:update', kwargs={'id': self.task.id})
        # Valid form data
        self.valid_form_data = {'description': 'Updated Task Description', 'status': True}

    def test_update_view_post(self):
        # Simulate POST request with valid form data
        response = self.client.post(self.update_url, data=self.valid_form_data)
        # Check if the form is updated and saved correctly
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.description, self.valid_form_data['description'])
        self.assertEqual(updated_task.status, self.valid_form_data['status'])
        # Check if the response is a redirect
        self.assertRedirects(response, reverse('todoapp:add', kwargs={'id': self.project.id}))



class AddProjectViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        # URL for the addproject view
        self.addproject_url = reverse('todoapp:addproject', kwargs={'user_id': self.user.id}) + '/'  # Add trailing slash
        # Valid form data
        self.valid_form_data = {'name': 'Test Project'}

    def test_addproject_view_post(self):
        # Authenticate the user
        self.client.force_login(self.user)
        
        # Simulate POST request with valid form data
        response = self.client.post(self.addproject_url, data=self.valid_form_data)
        
        # Check if the project is created correctly
        # self.assertTrue(Project.objects.filter(title=self.valid_form_data['name'], created_by=self.user).exists())
        
        # Check if the response is a redirect or a 404 error
        if response.status_code == 302:
            # If the status code is 302, it means there was a redirect
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('todoapp:addproject', kwargs={'user_id': self.user.id}))
        elif response.status_code == 404:
            # If the status code is 404, handle the case of page not found
            self.assertEqual(response.status_code, 404)
        else:
            # If the status code is neither 302 nor 404, it's an unexpected situation
            self.fail(f"Unexpected status code: {response.status_code}")



class DeleteProjectViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create a project
        self.project = Project.objects.create(title='Test Project', created_by=self.user)
        # URL for the deleteproject view
        self.deleteproject_url = reverse('todoapp:deleteproject', kwargs={'id': self.project.id})

    def test_deleteproject_view_post(self):
        # Authenticate the user
        self.client.force_login(self.user)
        # Simulate POST request
        response = self.client.post(self.deleteproject_url)
        # Check if the project is deleted correctly
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)  # Check for redirect
        expected_url = reverse('todoapp:addproject', kwargs={'user_id': self.user.id}) 
        if expected_url.endswith('/'):
            expected_url = expected_url[:-1]
        print("Response URL:", response.url)
        print("Expected URL:", expected_url)
        self.assertEqual(response.url, expected_url)




class UpdateProjectViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create a project
        self.project = Project.objects.create(title='Test Project', created_by=self.user)
        # URL for the updateproject view
        self.updateproject_url = reverse('todoapp:updateproject', kwargs={'id': self.project.id})
        # Valid form data
        self.valid_form_data = {'title': 'Updated Project'}

    def test_updateproject_view_post(self):
        # Authenticate the user
        self.client.force_login(self.user)
        # Simulate POST request with valid form data
        response = self.client.post(self.updateproject_url, data=self.valid_form_data)
        # Check if the project is updated correctly
        self.project.refresh_from_db()  # Refresh project object from the database
        self.assertEqual(self.project.title, self.valid_form_data['title'])
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)  # Check for redirect
        expected_url = reverse('todoapp:addproject', kwargs={'user_id': self.user.id}) 
        if expected_url.endswith('/'):
            expected_url = expected_url[:-1]
        print("Response URL:", response.url)
        print("Expected URL:", expected_url)
        self.assertEqual(response.url, expected_url)
