# -*- coding: utf-8 -*-

# from django.template import Context
# from django.utils.translation import ugettext
# from django.contrib.contenttypes.models import ContentType
from notification import backends
from notifications.models import Notification
from ignilife.utils import devices_for
import logging


logger = logging.getLogger("ignilife")


class MobileBackend(backends.BaseBackend):
    spam_sensitivity = 2
    synchronous = False

    def deliver(self, recipient, sender, notice_type, extra_context):
        # from ignilife.management import get_mobile_redirect_on_notification
        # target = get_mobile_redirect_on_notification(
        #     recipient, notice_type.label, extra_context.pop('target', None),
        #     sender)

        # Get the corrseponding on-site notification based on
        # its timestamp, sender, recipient, and notice_type
        # user_ctype = ContentType.objects.get(app_label="auth", model="user")
        try:
            notif = Notification.objects.get(
                timestamp=extra_context['timestamp'],
                # actor_content_type=user_ctype, actor_object_id=sender.pk,
                recipient=recipient, verb=notice_type.label)
            notification_id = notif.pk
        except Notification.DoesNotExist:
            notification_id = None

        for device in devices_for(recipient):
            try:
                device.send_message(
                    notice_type.description,
                    badge=recipient.notifications.filter(unread=True).count(),
                    extra={
                        "title": notice_type.display,
                        # "target": target
                        "notification_id": notification_id})
            except Exception, e:
                logger.error("Error while sending mobile notification: %s" % (
                    str(e),), extra={
                    'tags': {
                        'user_email': recipient.email,
                        'user': recipient.username
                    },
                    'device_registration_id': device.registration_id})

        # # If a target is given in the extra_context, retrieve it
        # target = extra_context.pop('target', None)

        # "recipient": recipient,
        # "title": ugettext(notice_type.display),
        # "description": ugettext(notice_type.description),

        # # context = self.default_context()
        # messages = self.get_formatted_messages((
        #     "notice.html",
        #     "full.html"
        # ), notice_type.label, Context(extra_context))
        # 'body': messages["notice.html"]

        # if not sender:
        #     sender = recipient
#
#         notify.send(
#             sender,
#             verb=notice_type.label,
#             target=target,
#             **extra_context)
