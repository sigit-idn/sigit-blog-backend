from ipaddress import ip_address
import re
from django.db import models
from django.utils import timezone

#######################################################################
# TABLES:
# 1. posts
# 2. images
# 3. comments
# 4. categories
#######################################################################

class Post(models.Model):
	"""
	class Post(models.Model):
		author, title, thumbnail, content, category, tags, views, reads, likes, dislikes, like_ip, dislike_ip, created_date, updated_date
	"""
	author        = models.ForeignKey   ('auth.User', on_delete=models.CASCADE						)
	title         = models.CharField    (max_length=200                       						)
	slug          = models.SlugField    (max_length=200, unique=True, 
																				default=str(title).lower().replace(' ', '-')		)
	thumbnail     = models.ImageField   (upload_to='.', blank=True            						)
	content       = models.TextField    (                                     						)
	category      = models.ForeignKey   ('Category', on_delete=models.SET_NULL, null=True	)
	tags          = models.TextField    (null=True                            						)
	views         = models.IntegerField (default=0                            						)
	reads         = models.IntegerField (default=0                            						)
	likes         = models.IntegerField (default=0                            						)
	dislikes      = models.IntegerField (default=0                            						)
	like_ip       = models.TextField    (default=''                           						)
	dislike_ip    = models.TextField    (default=''                           						)
	created_date  = models.DateTimeField(default=timezone.now                 						)
	updated_date  = models.DateTimeField(auto_now=True                        						)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def get_absolute_url(self):
		return "/blog/%s/" % self.slug

	def increment_views(self):
		self.views += 1
		self.save()

	def increment_reads(self):
		self.reads += 1
		self.save()

	def remove_duplicates(self):
		if self.like_ip:
			self.like_ip = ",".join(list(set(self.like_ip.split(','))))

		if self.dislike_ip:
			self.dislike_ip = ",".join(list(set(self.dislike_ip.split(','))))

	def increment_likes(self, ip_address):
		if self.like_ip:
			if ip_address in self.like_ip:
				self.like_ip = self.like_ip.replace(ip_address + ',', '')
				self.likes -= 1
				self.save()
				return False

		if self.dislike_ip:
			if ip_address in self.dislike_ip:
				self.dislike_ip = self.dislike_ip.replace(ip_address + ',', '')
				self.dislikes -= 1

		self.likes += 1
		self.like_ip = self.like_ip + ip_address + ','
		self.save()
		return True

	def increment_dislikes(self, ip_address):
		if self.dislike_ip:
			if ip_address in self.dislike_ip:
				self.dislike_ip = self.dislike_ip.replace(ip_address + ',', '')
				self.dislikes -= 1
				return False

		if self.like_ip:
			if ip_address in self.like_ip:
				self.like_ip = self.like_ip.replace(ip_address + ',', '')
				self.likes -= 1

		self.dislikes += 1
		self.dislike_ip = self.dislike_ip + ip_address + ','
		self.save()
		return True

	def __str__(self):
		return self.title

class Image(models.Model):
	"""
	class Image(models.Model):
		image, title, is_thumbnail, post, created_date
	"""
	image         = models.ImageField   (upload_to='.'                            )
	title         = models.CharField    (max_length=200                           )
	is_thumbnail  = models.BooleanField (default=False                            )
	post          = models.ForeignKey   (Post, on_delete=models.CASCADE, null=True)
	created_date  = models.DateTimeField(default=timezone.now                     )

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

class Comment(models.Model):
	"""
	class Comment(models.Model):
		author, nickname, post, content, created_date
	"""
	author        = models.TextField    (                              )
	nickname      = models.TextField    (                              )
	post          = models.ForeignKey   (Post, on_delete=models.CASCADE)
	content       = models.TextField    (                              )
	created_date  = models.DateTimeField(default=timezone.now          )

	def __str__(self):
		return self.content

class Category(models.Model):
	"""
	class Category(models.Model):
		name, created_date
	"""
	name          = models.CharField    (max_length=200      )
	created_date  = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name