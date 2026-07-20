import json
import base64
from requests import post, adapters, exceptions
from urllib.parse import urlencode

from .interface_bitrix_client import BitrixClientInterface


adapters.DEFAULT_RETRIES = 10


class BitrixClient(BitrixClientInterface):
    timeout = 10
    file_upload_timeout = 60

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def call(self, method, params, body=None):
        try:
            query_string = urlencode(params)
            url = self.webhook_url + '/' + method + '?' + query_string
            headers = {
                'Content-Type': 'application/json',
            }
            if body is not None:
                r = post(url, data=json.dumps(body), headers=headers, timeout=self.timeout)
            else:
                r = post(url, headers=headers, timeout=self.timeout)
            result = r.json()
        except exceptions.RequestException as e:
            print(f"RequestException occurred: {e}")
            return {"error": "RequestException", "message": str(e)}
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError occurred: {e}")
            return {"error": "JSONDecodeError", "message": str(e)}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {"error": "UnexpectedError", "message": str(e)}

        return result

    async def upload_file(self, url: str) -> str:
        try:
            response = post(url, timeout=self.file_upload_timeout)
            response.raise_for_status()

            file_content = response.content
            encoded_content = base64.b64encode(file_content).decode('utf-8')

            return encoded_content
        except exceptions.HTTPError as e:
            print(f"HTTPError occurred while uploading file: {e}")
            return ""
        except exceptions.ConnectionError as e:
            print(f"ConnectionError occurred while uploading file: {e}")
            return ""
        except exceptions.Timeout as e:
            print(f"Timeout occurred while uploading file: {e}")
            return ""
        except exceptions.RequestException as e:
            print(f"RequestException occurred while uploading file: {e}")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred while uploading file: {e}")
            return ""
