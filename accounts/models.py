from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from drugs.models import Drug


class UserManager(BaseUserManager):
    def create_user(self, username, nickname, email, password=None):
        if not email:
            raise ValueError('이메일은 필수입니다.')

        user = self.model(
            username=username,
            nickname=nickname,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nickname, email, password):
        user = self.create_user(
            username=username,
            nickname=nickname,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField('아이디', max_length=30, unique=True)
    password = models.CharField('비밀번호', max_length=255)
    nickname = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    profile_img = models.ImageField(upload_to='media/userProfile',
                                    default='media/userProfile/default.png',
                                    blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email_verification_token = models.CharField(
        max_length=100, null=True, blank=True)
    is_active = models.BooleanField('계정 활성화 여부', default=False)
    is_admin = models.BooleanField('관리자 여부', default=False)
    updated_at = models.DateField('수정일', auto_now=True)
    durgslist = models.ManyToManyField(Drug, blank=True, related_name='takers')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'username', 'password']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
