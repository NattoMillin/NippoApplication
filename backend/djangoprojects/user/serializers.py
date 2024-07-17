from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


# ユーザー情報のシリアライザ
class UserSerializer(serializers.ModelSerializer):
    # uidフィールドは読み取り専用
    uid = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"