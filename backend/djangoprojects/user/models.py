from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from hashids import Hashids


# カスタムユーザーマネージャークラス
class UserManager(BaseUserManager):
    # 通常ユーザー作成メソッド
    def create_user(self, number, password, **extra_fields):
        # メールアドレスの検証

        # ユーザーオブジェクトの作成と保存
        user = self.model(number=number, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    # スーパーユーザー作成メソッド
    def create_superuser(self, number, password, **extra_fields):
        user = self.create_user(number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


# カスタムユーザーアカウントモデル
class UserAccount(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField("uid", max_length=30, unique=True, null=True)
    number = models.CharField("従業員番号", max_length=6, unique=True)
    name = models.CharField("名前", max_length=255)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    # アクティブ状態とスタッフ権限フィールド
    is_active = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # ユーザーマネージャーと認証フィールドの設定
    objects = UserManager()
    USERNAME_FIELD = "number"
    REQUIRED_FIELDS = []

    def get_short_name(self):
        return self.name  # first_name を返す例

    class Meta:
        verbose_name = "ユーザーアカウント"
        verbose_name_plural = "ユーザーアカウント"

    def __str__(self):
        return self.name


# アカウントが作成された後に実行されるシグナルレシーバー
@receiver(post_save, sender=UserAccount)
def generate_random_user_uid(sender, instance, created, **kwargs):
    # 新規作成時にランダムUIDを生成
    if created:
        hashids = Hashids(salt="xRXSMT8XpzdUbDNM9qkv6JzUezU64D4Z", min_length=8)
        instance.uid = hashids.encode(instance.id)
        instance.save()
