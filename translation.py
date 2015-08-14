from modeltranslation.translator import register, TranslationOptions

from .models import NoticeType

@register(NoticeType)
class NoticeTypeTranslationOptions (TranslationOptions):
    fields = ('display', 'description')
