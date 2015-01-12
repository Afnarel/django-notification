from models import NOTICE_MEDIA, NoticeType, NoticeSetting

__version__ = "1.1.1"


def can_send(user, notice_type_id, backend_name):
    """
    For instance: can_send(afnarel, 'ignilife_news', 'email')
    """
    notice_type = NoticeType.objects.get(label=notice_type_id)

    backend_id = None
    for bid, bname in NOTICE_MEDIA:
        if bname == backend_name:
            backend_id = bid
            break
    if backend_id is None:
        return False

    return NoticeSetting.for_user(user, notice_type, backend_id).send
