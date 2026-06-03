
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/avatar-placeholder.png'
    
class EmailConfirm(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	code=models.CharField(max_length=6)

	def __str__(self):
		return self.user.username
# Create your models here.
