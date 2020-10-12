from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['username', 'is_active', 'server_type']


admin.site.register(User, UserAdmin)
admin.site.site_header = '信乘数据 VPN管理平台'
admin.site.site_title = 'VPN后台管理'
admin.site.index_title = '信乘数据'