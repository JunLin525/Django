from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 8



class QuestionAdmin(admin.ModelAdmin):
    def uuid_hex(self, obj):
        return str(obj.id.hex)
    uuid_hex.short_description = 'ID'
    
    fieldsets = [
        ('QuestionContent',               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('id','question_text', 'pub_date', 'was_published_recently', 'get_user')
    list_filter = ['pub_date']
    search_fields = ['question_text','id']
    #inlines = [remark]

    def get_user(self, obj):
        return obj.user.username
    get_user.admin_order_field = 'user__username'
    get_user.short_description='User'


admin.site.register(Question, QuestionAdmin)
