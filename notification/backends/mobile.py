# -*- coding: utf-8 -*-

# from django.template import Context
# from django.utils.translation import ugettext
from notification import backends
from ignilife.utils import devices_for


class MobileBackend(backends.BaseBackend):
    spam_sensitivity = 2

    def deliver(self, recipient, sender, notice_type, extra_context):
        from ignilife.management import get_mobile_redirect_on_notification
        target = get_mobile_redirect_on_notification(
            recipient, notice_type.label, extra_context.pop('target', None))
        for device in devices_for(recipient):
            device.send_message(notice_type.description, extra={
                "title": notice_type.display,
                "target": target})

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
