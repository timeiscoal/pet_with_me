from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username=None,introduce=None ,password=None):
        if not email:
            raise ValueError("이메일을 입력해주세요.")

        email =self.normalize_email(email)

        user = self.model(email=email, username= username , introduce=introduce)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None,introduce=None ,password=None):
        
        user = self.create_user(email =self.normalize_email(email),
                                username=username,
                                introduce=introduce,
                                password=password)
        user.is_admin = True
        user.is_superuser =True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    introduce = models.CharField(max_length=200,blank=True,null=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    us_staff = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    profile_img = models.ImageField(upload_to="media/user", null=True,blank=True)

    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []