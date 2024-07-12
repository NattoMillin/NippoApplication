from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdminCustom(UserAdmin):
    # 詳細
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uid",
                    "number",
                    "name",
                    "email",
                    "password",
                    "is_active",
                    "is_manager",
                    "is_staff",
                    "is_superuser",
                    "updated_at",
                    "created_at",
                )
            },
        ),
    )

    # 追加
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "number",
                    "name",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_manager",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    # 一覧
    list_display = (
        "uid",
        "number",
        "name",
        "email",
        "is_active",
        "updated_at",
        "created_at",
    )

    list_filter = ()
    # 検索
    search_fields = (
        "uid",
        "number",
    )
    # 順番
    ordering = ("updated_at",)
    # リンク
    list_display_links = ("uid", "name", "number")
    # 編集不可
    readonly_fields = ("updated_at", "created_at", "uid")


admin.site.register(User, UserAdminCustom)
