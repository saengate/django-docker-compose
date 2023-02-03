from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _


class ForSession(object):

    @staticmethod
    def t(request, msg):
        try:
            language_from_session = request.session.get(translation.LANGUAGE_SESSION_KEY)
            if language_from_session:
                language = language_from_session
            else:
                language = 'en'
                request.session[translation.LANGUAGE_SESSION_KEY] = 'en'

            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()

            msg = _(msg)
        finally:
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = translation.get_language()
        return {
            'msg': msg,
            'request': request
        }


translate = ForSession.t
