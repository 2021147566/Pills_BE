from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from drugs.models import Drug
from django.urls import reverse
from allauth.account.models import EmailAddress


class UserManager(BaseUserManager):
    def create_user(self, username, nickname, email, password=None):
        if not email:
            raise ValueError("이메일은 필수입니다.")

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
    username = models.CharField("아이디", max_length=30, unique=True)
    password = models.CharField("비밀번호", max_length=255)
    nickname = models.CharField(max_length=20, unique=False)
    email = models.EmailField(unique=True)
    profile_img = models.ImageField(
        upload_to="media/userProfile",
        default="media/userProfile/default.png",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField("관리자 여부", default=False)
    updated_at = models.DateField("수정일", auto_now=True)
    durgslist = models.ManyToManyField(Drug, blank=True, related_name="takers")
    verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "username", "password"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse("my_page_view", kwargs={"user_id": self.pk})

    def email_verified(self):
        try:
            return self.email.get(primary=True).verified
        except EmailAddress.DoesNotExist:
            return False

    @property
    def is_staff(self):
        return self.is_admin
