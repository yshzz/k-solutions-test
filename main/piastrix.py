import requests
from validators import url as url_validator
from hashlib import sha256
from .exceptions import PiastrixApiException

BASE_URL = 'https://core.piastrix.com/'
PAYWAY = 'payeer_rub'


class BaseApi:
    """Base class for API interaction.

    Args:
        shop_id (:obj:`str`): Shop ID in the Piastrix system.
        secret_key (:obj:`str`): Secret key used to sign requests.
    """

    def __init__(self, secret_key, base_url):
        self.secret_key = secret_key
        self.base_url = base_url

    def _post(self, endpoint, body):
        url = self._form_url(endpoint)
        return requests.post(url, json=body)

    def get_data(self, endpoint, body):
        """Process HTTP response.

        Use this method everytime you need to make API request.

        Args:
            enpoint (:obj:`str`): Path where to execute request.
            body (:obj:`dict`): HTTP request body.
        Returns:
            :obj:`dict`: Response data.
        Raises:
            :class:`main.piastrix.PiastrixException`: Piastrix error.
        """

        response_content = self._post(endpoint, body).json()

        if response_content['result'] is False:
            raise PiastrixApiException(response_content['message'],
                                       response_content['error_code'])

        return response_content['data']

    def _sign(self, data, required_fields):
        sorted_data = [str(data[key]) for key in sorted(required_fields)]
        signed_data = ':'.join(sorted_data) + self.secret_key
        data['sign'] = sha256(signed_data.encode('utf-8')).hexdigest()

    def _form_url(self, endpoint):
        # Typical case for url forming.
        typical_case = self.base_url + endpoint

        if self.base_url.endswith('/'):
            formed_url = typical_case if not endpoint.startswith('/') else self.base_url[:-1] + endpoint
        else:
            formed_url = typical_case if endpoint.startswith('/') else self.base_url + '/' + endpoint

        if url_validator(formed_url):
            return formed_url
        else:
            raise ValueError(f'Url "{formed_url}" is not valid!')


class Piastrix(BaseApi):
    """Piastrix client.

    Args:
        shop_id (:obj:`str`): Shop ID in the Piastrix system.
        secret_key (:obj:`str`): Secret key used to sign requests.
        base_url (:obj:`str`): API base url.
    """

    def __init__(self, shop_id, secret_key, base_url=BASE_URL):
        super().__init__(secret_key, base_url)
        self.shop_id = shop_id

    def bill(self, shop_amount, shop_currency, payer_currency,
             shop_order_id, description=None):
        """Bill method.

        Args:
            shop_amount (:obj:`float`)
            shop_currency (:obj:`int`)
            payer_currency (:obj:`int`)
            shop_order_id (:obj:`str`)
            description (:obj:`str`, optional)
        """

        required_fields = [
            'shop_amount',
            'shop_currency',
            'shop_id',
            'shop_order_id',
            'payer_currency'
        ]

        body = {
            "shop_amount": shop_amount,
            "shop_currency": shop_currency,
            "payer_currency": payer_currency,
            "shop_order_id": shop_order_id,
            "shop_id": self.shop_id
        }

        if description:
            body['description'] = description

        self._sign(body, required_fields)
        return self.get_data('bill/create', body)

    def invoice(self, amount, currency, shop_order_id,
                payway=PAYWAY, description=None):
        """Invoice method.

        Args:
            amount (:obj:`float`)
            currency (:obj:`int`)
            shop_order_id (:obj:`str`)
            payway (:obj:`str`)
            description (:obj:`str`, optional)
        """

        required_fields = [
            'amount',
            'currency',
            'payway',
            'shop_id',
            'shop_order_id'
        ]

        body = {
            "amount": amount,
            "currency": currency,
            "shop_order_id": shop_order_id,
            "payway": payway,
            "shop_id": self.shop_id
        }

        if description:
            body['description'] = description

        self._sign(body, required_fields)
        return self.get_data('invoice/create', body)

    def pay(self, amount, currency, description, shop_order_id, lang='ru'):
        """Pay method.

        Args:
            amount (:obj:`float`)
            currency (:obj:`int`)
            description (:obj:`str`)
            shop_order_id (:obj:`str`)
            lang (:obj:`str`)
        """

        if lang not in ('ru', 'en'):
            raise ValueError(f'{lang} is not valid language')

        required_fields = [
            'amount',
            'currency',
            'shop_id',
            'shop_order_id'
        ]

        form_data = {
            "amount": amount,
            "currency": currency,
            "description": description,
            "shop_order_id": shop_order_id,
            "shop_id": self.shop_id
        }

        self._sign(form_data, required_fields)
        return form_data, f"https://pay.piastrix.com/{lang}/pay"
