from django.conf import settings
# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from notification import backends
import logging
import sys

logger = logging.getLogger("ignilife")


class EmailBackend(backends.BaseBackend):
    spam_sensitivity = 2

    def can_send(self, user, notice_type):
        can_send = super(EmailBackend, self).can_send(user, notice_type)
        if can_send and user.email:
            return True
        return False

    def deliver(self, recipient, sender, notice_type, extra_context):
        # TODO: require this to be passed in extra_context

        context = self.default_context()
        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.display),
        })
        context.update(extra_context)

        messages = self.get_formatted_messages((
            "short.txt",
            "full.txt",
            "full.html"
        ), notice_type.label, context)

        subject = "".join(render_to_string("notification/email_subject.txt", {
            "message": messages["short.txt"],
        }, context).splitlines())

        body = render_to_string("notification/email_body.txt", {
            "message": messages["full.txt"],
        }, context)

        body_html = render_to_string("notification/email_body.html", {
            "message": messages["full.html"],
        }, context)

        try:
            msg = EmailMultiAlternatives(
                subject, body, settings.DEFAULT_FROM_EMAIL, [recipient.email])
            msg.attach_alternative(body_html, "text/html")
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()

            # send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
            #           [recipient.email])
        except:
            logger.error(
                "Mail could not be sent to email %s (user: %s) for notice type '%s'. Exception: %s" % (
                    recipient.email, recipient.username, notice_type, sys.exc_info()[0]))
