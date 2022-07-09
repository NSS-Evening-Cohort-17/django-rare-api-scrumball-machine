from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from rareapi.models import Post

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
    
class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved')
        depth = 2    

class CreatePostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved')    