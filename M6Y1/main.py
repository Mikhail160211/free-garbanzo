import json
import time
import requests
import base64
from PIL import Image
from io import BytesIO


import requests
#F43936049E39DC898F77E624F08B3DA5
#832E35AA7AEB03D13EC85B6620EFC5BC


class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)











    def save_image(self, base64_string, file_path):
        

# Декодируем строку Base64 в бинарные данные
        decoded_data = base64.b64decode(base64_string)
# Создаем объект изображения с помощью PIL
        image = Image.open(BytesIO(decoded_data))
        image = image.save(file_path)
# Отображаем изображение (опционально)
        












if __name__ == '__main__':
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', 'F43936049E39DC898F77E624F08B3DA5', '832E35AA7AEB03D13EC85B6620EFC5BC')
    pipeline_id = api.get_pipeline()
    uuid = api.generate("cat", pipeline_id)
    files = api.check_generation(uuid)
    api.save_image(files[0],"generating_image.png")
    
    



    