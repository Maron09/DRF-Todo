from rest_framework import serializers
from .models import Category, Todo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']



class TodoSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'category']