from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,ChatData,PersonalToken,Users,GroupToken,UserGroup,GroupData
# Register your models here.

class GroupAdmin(admin.ModelAdmin):
    list_display = ['id','admin','groupname','group_uuid','created_time']
    actions = None

class GroupDataAdmin(admin.ModelAdmin):
    list_display = ['id','username','is_enable','created_time']
    

class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['id','admin','groupname','picture','group_uuid','created_time']
    actions = None
    
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id','sender','receiver','hidden','created_time']
    actions = None

class PersonalAdmin(admin.ModelAdmin):
    list_display = ['id','sender','receiver','Token','created_time']
    actions = None

class userAdmin(UserAdmin):
    list_display = ['id','email','username','is_staff','is_active','is_superuser','uuid']
    list_filter = ['is_staff','is_superuser','is_active']
    search_fields = ['id','username','email','first_name','last_name']

    fieldsets = (
        (None,{'fields':('email','password')}),
        ('personal information',{'fields':('first_name','last_name','phone_number')}),
        ('permissions',{'fields':('is_active','is_staff','is_superuser')})
    )

    add_fieldsets = (
        (None,{'classes':('wide',),
                'fields':('email','first_name','last_name','phone_number','password1','password2','is_active','is_staff','is_superuer')}
                ),

    )


class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','uuid_id','uuid_name','uuid']

admin.site.register(GroupToken,GroupAdmin)
admin.site.register(ChatData,ChatAdmin)
admin.site.register(PersonalToken,PersonalAdmin)
admin.site.register(UserGroup,UserGroupAdmin)
admin.site.register(CustomUser,userAdmin)
admin.site.register(Users,UserAdmin)
admin.site.register(GroupData,GroupDataAdmin)
