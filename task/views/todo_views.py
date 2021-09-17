from rest_framework import views, status
from rest_framework.response import Response

from task.models.todo import Todo


class TodoAPIView(views.APIView):

    def post(self, request):
        title = request.data.get('title')
        is_active = request.data.get('is_active')
        todo = Todo.objects.create(title=title, is_active=is_active)
        return Response(todo, status=status.HTTP_201_CREATED)
