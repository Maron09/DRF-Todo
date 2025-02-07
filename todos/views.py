from .serializers import CategorySerializer, TodoSerializer
from .models import Todo, Category
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404



class CategoryView(GenericAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    
    def get_queryset(self):
        
        return Category.objects.filter(user=self.request.user)
    
    def get(self, request):
        categories = self.get_queryset()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CategoryDetail(GenericAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    
    
    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
            if category.user != self.request.user:
                return Response({"error": "You do not have permission to access this Category."}, status=status.HTTP_403_FORBIDDEN) 
            return category
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        category = self.get_object(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        category = self.get_object(pk=pk)
        serializer = self.serializer_class(category, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Category Updated Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = self.get_object(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class TodoView(GenericAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    
    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        queryset = Todo.objects.filter(user=self.request.user)
        
        if status_param:
            queryset = queryset.filter(status=status_param)
            
        return queryset
    
    def get(self, request):
        todos = self.get_queryset()
        serializer = self.serializer_class(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "TODO Added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailView(GenericAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        """Ensure that the requested todo belongs to the authenticated user."""
        try:
            todo = Todo.objects.get(pk=pk)
            if todo.user != self.request.user:
                return Response({"error": "You do not have permission to access this todo."}, status=status.HTTP_403_FORBIDDEN)
            return todo
        except Todo.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Retrieve a single todo if the user owns it."""
        todo = self.get_object(pk)
        serializer = self.serializer_class(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        todo = self.get_object(pk)
        serializer = self.serializer_class(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "TODO Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a todo if the user owns it."""
        todo = self.get_object(pk)
        todo.delete()
        return Response({"message": "TODO Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)