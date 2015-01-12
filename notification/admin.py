from django.contrib import admin

from notification.models import NoticeType, NoticeSetting, NoticeQueueBatch


class NoticeTypeAdmin(admin.ModelAdmin):
    list_display = ["label", "display", "description", "default"]


class NoticeSettingAdmin(admin.ModelAdmin):
    list_display = ["user", "notice_type", "medium", "send"]
    search_fields = ['user__username']


admin.site.register(NoticeQueueBatch)
admin.site.register(NoticeType, NoticeTypeAdmin)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
