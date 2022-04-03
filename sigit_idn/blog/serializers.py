from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.db import models
from django.utils import timezone
from sigit_idn.blog.models import Post, Image, Comment, Category

#########################################################################
# SERIALIZERS:
# 1. posts
# 2. images
# 3. comments
# 4. categories
#########################################################################

class PostSerializer(serializers.ModelSerializer):
	"""
	class PostSerializer(serializers.ModelSerializer):
		author, title, slug, thumbnail, content, category, tags, views, reads, likes, dislikes, like_ip, dislike_ip, created_date, updated_date
	"""
	author = serializers.ReadOnlyField(source='author.username')
	class Meta:
		model = Post
		fields = '__all__'
		lookup_field = 'slug'
		extra_kwargs = {
			'url': {'lookup_field': 'slug'}
		}

class ImageSerializer(serializers.ModelSerializer):
	"""
	class ImageSerializer(serializers.ModelSerializer):
		image, title, is_thumbnail, post, created_date
	"""
	image = serializers.ImageField()
	class Meta:
		model = Image
		fields = ('image', 'title', 'is_thumbnail', 'post', 'created_date')

class CommentSerializer(serializers.ModelSerializer):
	"""
	class CommentSerializer(serializers.ModelSerializer):
		author, nickname, post, content, created_date
	"""
	author = serializers.ReadOnlyField(source='author.username')
	class Meta:
		model = Comment
		fields = ('author', 'post', 'content', 'created_date')

class CategorySerializer(serializers.ModelSerializer):
	"""
	class CategorySerializer(serializers.ModelSerializer):
		name, created_date
	"""
	class Meta:
		model = Category
		fields = ('name', 'created_date')