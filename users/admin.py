from django.contrib import admin
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'username',
        'last_name',
        'first_name',
        'email',
        'position',
        'section',
    )

    search_fields = (
        'username',
        'last_name',
        'first_name',
        'section__name',
    )
    
    list_filter = (
        'section__name',
    )

    # fieldsets = (
    #     ("기본 정보", {
    #         "fields": (
    #             'username',
    #             'password',
    #         ),
    #     }),
    # )
    
    
