from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serialize import UserSerializer, TodoSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Todo

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token) 
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

    def get(self, request):
        return Response({'detail': 'Method "GET" not allowed.'}, status=405)
        
        
class TokenRefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        print(refresh_token)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                access_token = str(token.access_token)
                return Response({'access_token': access_token}, status=200)
            except Exception as e:
                return Response({'error': 'Invalid or expired refresh token'}, status=400)
        else:
            return Response({'error': 'Refresh token not provided'}, status=400)


class TodoCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        todos = Todo.objects.filter(user=user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
class TodoUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id, user=request.user)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, todo_id):
        print(todo_id,request.user)
        try:
            todo = Todo.objects.get(id=todo_id, user=request.user)
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
  