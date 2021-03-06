from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import UserProfileInfo, User

class ProfileInline(admin.StackedInline):
    model = UserProfileInfo
    can_delete = False
    verbose_name_plural = 'UserProfileInfo'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register your models here.
admin.site.register(UserProfileInfo)
