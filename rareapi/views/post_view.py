from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from rareapi.models import Post, RareUser


class PostView(ViewSet):
    """Rare Event View"""
    
    def retrieve(self, request, pk):
        """Handle Get request for a single post
        
        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all post
        
        Returns:
            Response -- JSON serialized list of post
        """
        posts = Post.objects.all()
        category = request.query_params.get('category', None)
        if category is not None:
             posts = posts.filter(category_id=category)
             
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized event instance
        """
        rareuser = RareUser.objects.get(user=request.auth.user)
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rareuser=rareuser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a Post

        Returns:
            Response -- Empty body with 204 status code
        """
        post = Post.objects.get(pk=pk)
        serializer = CreatePostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('id', 'rareuser', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved')
        depth = 2    

class CreatePostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('id', 'rareuser', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved')    