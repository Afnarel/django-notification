from django.contrib import admin
from notification.models import NoticeType, NoticeSetting, NoticeQueueBatch
from django.contrib.auth.models import User


class NoticeQueueBatchAdmin(admin.ModelAdmin):
    list_display = ["user", "label", "extra_context", "sender"]

    def user(self, notice):
        user_id = notice.deserialize()[0]
        try:
            user = User.objects.get(pk=user_id)
            return user.username
        except User.DoesNotExist:
            return user_id

    def label(self, notice):
        return notice.deserialize()[1]

    def extra_context(self, notice):
        return notice.deserialize()[2]

    def sender(self, notice):
        return notice.deserialize()[3]


class NoticeTypeAdmin(admin.ModelAdmin):
    list_display = ["label", "display", "description", "default"]


class NoticeSettingAdmin(admin.ModelAdmin):
    list_display = ["user", "notice_type", "medium", "send"]
    search_fields = ['user__username']


admin.site.register(NoticeQueueBatch, NoticeQueueBatchAdmin)
admin.site.register(NoticeType, NoticeTypeAdmin)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
