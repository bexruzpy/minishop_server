from django.contrib import admin

from .models import User, DeviceToken

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'device_id', "has_profile"]
    # Muhim vaqtlar
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'phone', 'device_id']
    readonly_fields = ['has_profile', 'device_id', 'created_at', 'updated_at']
    
    
    def has_profile(self, obj):
        return hasattr(obj, "devicetoken")
    has_profile.boolean = True
    has_profile.short_description = "Sotib olganmi"
    def get_readonly_fields(self, request, obj=None):
        if obj:  # agar mavjud obyekt bo'lsa (edit page)
            return ['has_profile', 'device_id', 'created_at', 'updated_at']
        return ['has_profile', 'created_at', 'updated_at']

@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token_view']
    readonly_fields = ['user', 'token', 'created_at', 'updated_at']
    def get_readonly_fields(self, request, obj=None):
        if obj:  # agar mavjud obyekt bo'lsa (edit page)
            return ['user', 'token', 'created_at', 'updated_at']
        return ['token', 'created_at', 'updated_at']  # faqat add page da user va token editable
    def token_view(self, obj):
        return obj.token.get("data")
    token_view.short_description = "Token"
    # create form
    def foydalanuvchi(self, obj):
        return obj.user
    foydalanuvchi.short_description = "Foydalanuvchi"



