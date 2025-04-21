import os
import json
import requests

class PaymentManager:
    def __init__(self, personal_code):
        self.personal_code = personal_code

        self._api_get_balance_url = os.environ.get('YALLVEND_API_BALANCE_URL')
        self._api_product_price_url = os.environ.get('YALLVEND_API_PRODUCT_PRICE_URL')
        self._api_payment_url = os.environ.get('YALLVEND_API_PAYMENT_URL')
        self._api_get_balance_referer = os.environ.get('YALLVEND_REFERER_BALANCE')
        self._api_payment_referer_base = os.environ.get('YALLVEND_REFERER_PAYMENT_BASE')

        self._api_key_balance = os.environ.get('YALLVEND_API_KEY')
        self._api_key_price = os.environ.get('YALLVEND_PRICE_KEY')

    def get_balance(self):
        headers = {
            'Content-Type': 'application/json',
            'Referer': self._api_get_balance_referer
        }
        payload = {
            'country': 'tw',
            'key': self._api_key_balance,
            'id': self.personal_code
        }
        try:
            response = requests.post(self._api_get_balance_url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()
            result = response.json()
            return int(float(result.get('point', 0)))
        except Exception as e:
            return {"error": str(e)}

    def get_current_product_price(self, vid):
        form_data = {
            'key': self._api_key_price,
            'func': 'loadDefaultAmount',
            'vidCode': vid
        }
        try:
            response = requests.post(self._api_product_price_url, data=form_data, timeout=5)
            response.raise_for_status()
            result = response.json()
            return result.get('defaultAmount', 0)
        except Exception as e:
            return {"error": str(e)}

    def pay(self, price, vid):
        data = {
            'vid': vid,
            'amount': str(price),
            'staff_id': self.personal_code,
            'uuid': '111',
            'haveAuth': False
        }

        encoded_data = "data=" + requests.utils.quote(json.dumps(data))

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': self._api_payment_referer_base + vid
        }
        try:
            response = requests.post(self._api_payment_url, data=encoded_data, headers=headers, timeout=5)
            response.raise_for_status()
            result = response.json()
            return result.get('status', 'unknown')
        except Exception as e:
            return {"error": str(e)}
