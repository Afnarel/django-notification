# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from ignilife import messages
from django.utils.translation import ugettext as _

from django.contrib.auth.decorators import login_required

from notification.models import NoticeSetting, NoticeType, NOTICE_MEDIA


def notice_settings_helper(request, data=None):
    notice_types = NoticeType.objects.all()
    settings_table = []
    for notice_type in notice_types:
        settings_row = []
        for medium_id, medium_display in NOTICE_MEDIA:
            if medium_display == 'site':
                continue
            form_label = "%s_%s" % (notice_type.label, medium_id)
            setting = NoticeSetting.for_user(
                request.user, notice_type, medium_id)
            if request.method == "POST":
                if data is None:
                    data = request.POST
                if data.get(form_label) == "on":
                    if not setting.send:
                        setting.send = True
                        setting.save()
                else:
                    if setting.send:
                        setting.send = False
                        setting.save()
            settings_row.append((form_label, setting.send))
        settings_table.append({
            "notice_type": notice_type,
            "cells": settings_row})

    if request.method == "POST":
        messages.success(request, _(u"Vos données ont bien été enregistrées."))

    settings = {
        "column_headers": [medium_display for medium_id, medium_display in
                           NOTICE_MEDIA if medium_display != 'site'],
        "rows": settings_table,
    }

    return {
        "notice_types": notice_types,
        "notice_settings": settings,
    }


@login_required
def notice_settings(request):
    """
    The notice settings view.

    Template: :template:`notification/notice_settings.html`

    Context:

      * notice_types
        A list of all :model:`notification.NoticeType` objects.

      * notice_settings
        A dictionary containing ``column_headers`` for each ``NOTICE_MEDIA``
        and ``rows`` containing a list of dictionaries: ``notice_type``, a
        :model:`notification.NoticeType` object and ``cells``, a list of
        tuples whose first value is suitable for use in forms and the second
        value is ``True`` or ``False`` depending on a ``request.POST``
        variable called ``form_label``, whose valid value is ``on``.
    """

    data = notice_settings_helper(request)
    return render_to_response("notification/notice_settings.html", data,
                              context_instance=RequestContext(request))
