from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from todo.models import Todo

# Create your tests here.


class TodoTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="testowner", password="testpass")
        self.client.login(username="testowner", password="testpass")
        self.validate_data = {
            "title": "Todo DRF Testing",
            "description": "Write unit test for Todo APIs",
            "priority": 1
        }

    def test_create_todo_sucess(self):
        response = self.client.post(
            "/todo/", self.validate_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.first().title, "Todo DRF Testing")

    def test_list_todos(self):
        Todo.objects.create(owner=self.owner, title="Todo 1",
                            description="desc 1")
        Todo.objects.create(owner=self.owner, title="Todo 2",
                            description="desc 2")
        response = self.client.get("/todo/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_todo(self):
        todo = Todo.objects.create(
            owner=self.owner, title="Todo 1", description="desc 1")
        response = self.client.patch(
            f"/todo/{todo.id}/", {"title": "Updated Todo title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.get(
            id=todo.id).title, "Updated Todo title")

    def test_delete_todo(self):
        todo = Todo.objects.create(
            owner=self.owner, title="Todo 1", description="desc 1")
        response = self.client.delete(f"/todo/{todo.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(pk=todo.id).exists())
