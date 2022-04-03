from asyncore import read
from django.urls import path
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action
from sigit_idn.blog.models import Post, Image, Comment, Category
from sigit_idn.blog.serializers import PostSerializer, ImageSerializer, CommentSerializer, CategorySerializer

#######################################################################
# VIEWS:
# 1. posts
# 2. images
# 3. comments
# 4. categories
#######################################################################

class PostViewSet(viewsets.ModelViewSet):
	"""
    API endpoint that allows users to be viewed or edited.
	"""
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	lookup_field = 'slug'

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

	@action(detail=True, methods=['get'], url_path='like')
	def like(self, request, slug=None):
		post = self.get_object()
		ip_address = request.META['REMOTE_ADDR']
		like_result = post.increment_likes(ip_address)
		
		response = {
			'message': 'You have liked this post.' if like_result else 'Your like has been removed.',
			'likes': post.likes,
			'dislikes': post.dislikes,
		}

		return Response(response)

	@action(detail=True, methods=['get'], url_path='dislike')
	def dislike(self, request, slug=None):
		post = self.get_object()
		ip_address = request.META['REMOTE_ADDR']
		dislike_result = post.increment_dislikes(ip_address)

		response = {
			'message': 'You have disliked this post.' if dislike_result else 'Your dislike has been removed.',
			'likes': post.likes,
			'dislikes': post.dislikes,
		}

		return Response(response)

	@action(detail=True, methods=['get'], url_path='read')
	def read(self, request, slug=None):
		post = self.get_object()
		read_result = post.increment_reads()

		response = {
			'message': 'You have read this post.' if read_result else 'Your read has been removed.',
			'reads': post.reads,
		}

		return Response(response)

	@action(detail=True, methods=['get'], url_path='view')
	def view(self, request, slug=None):
		post = self.get_object()
		post.increment_views()
		return Response({'views': post.views})

class ImageViewSet(viewsets.ModelViewSet):
	"""
		API endpoint that allows users to be viewed or edited.
	"""
	queryset = Image.objects.all()
	serializer_class = ImageSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
	"""
		API endpoint that allows users to be viewed or edited.
	"""
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
	"""
		API endpoint that allows users to be viewed or edited.
	"""
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)