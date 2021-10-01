from rest_framework import views, status
from rest_framework.response import Response

from task.models.todo import Todo
from task.serializers.todo_serializer import TodoSerializer


class TodoAPIView(views.APIView):

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=TodoSerializer):
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        todo = Todo.objects.all()
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
