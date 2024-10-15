from typing import Optional

import requests
import urllib3


class GigaChatService:
    def __init__(self, secret_key: str):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.secret_key = secret_key
        self.token: Optional[str] = None

    def _get_token(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': '784ef77e-618d-4ea9-b024-d47c6526b336',
            'Authorization': f'Basic {self.secret_key}'
        }
        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }
        response = requests.request("POST", "https://ngw.devices.sberbank.ru:9443/api/v2/oauth", headers=headers,
                                    data=payload, verify=False)
        self.token = response.json().get("access_token")

    def _check_token(self) -> bool:
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.get('https://gigachat.devices.sberbank.ru/api/v1/models', headers=headers, verify=False)
        if response.status_code < 400:
            return True
        return False

    def _get_answer(self, text: str) -> str:
        if self.token and self._check_token():
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.token}',
            }
            json_data = {
                'model': 'GigaChat',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'Ты персональный ассистент',
                    },
                    {
                        'role': 'user',
                        'content': text,
                    },
                ],
                'stream': False,
                'update_interval': 0,
            }

            response = requests.post('https://gigachat.devices.sberbank.ru/api/v1/chat/completions', headers=headers,
                                     json=json_data, verify=False)
            try:
                return response.json().get("choices", [])[0].get("message", {}).get("content", "")
            except IndexError:
                return ""
        else:
            self._get_token()
            return self._get_answer(text)

    def request(self, text: str) -> None:
        print(f"\n\n{self._get_answer(text)}")
