# -*- coding: utf-8 -*-

from django.template import Context
from django.utils.translation import ugettext

from notification import backends
from notifications import notify


class SiteBackend(backends.BaseBackend):
    spam_sensitivity = 2

    def deliver(self, recipient, sender, notice_type, extra_context):

        extra_context.update({
            "recipient": recipient,
            "notice_type": notice_type.label,
            "title": ugettext(notice_type.display),
            "from_username": sender.username
        })

        # context = self.default_context()
        messages = self.get_formatted_messages((
            "notice.html",
            "full.html"
        ), notice_type.label, Context(extra_context))

        extra_context.update({
            'body': messages["notice.html"]
        })

        print sender
        print dir(sender)
        notify.send(
            sender,
            verb=ugettext(notice_type.description),
            **extra_context)
