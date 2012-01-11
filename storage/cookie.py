from django.core.exceptions import SuspiciousOperation
from formwizard.utils import BadSignature
from django.utils import simplejson as json

from formwizard import storage


class CookieStorage(storage.BaseStorage):
    encoder = json.JSONEncoder(separators=(',', ':'))

    def __init__(self, *args, **kwargs):
        super(CookieStorage, self).__init__(*args, **kwargs)
        self.data = self.load_data()
        if self.data is None:
            self.init_data()

    def load_data(self):
        try:
            data = self.request.COOKIES[self.prefix] # TODO: get_signed_cookie in django 1.4
        except KeyError:
            data = None
        except BadSignature:
            raise SuspiciousOperation('WizardView cookie manipulated')
        if data is None:
            return None
        return json.loads(data, cls=json.JSONDecoder)

    def update_response(self, response):
        if self.data:
            response.set_cookie(self.prefix, self.encoder.encode(self.data)) # TODO: set_signed_cookie in django 1.4
        else:
            response.delete_cookie(self.prefix)
