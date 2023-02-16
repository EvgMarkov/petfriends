
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class APIRequest:
    """API библиотека к сайту Pet Friends"""
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> json:
        """"Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""
        headers = {
            'email': email,
            'password': password,
        }

        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """"Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фльтр может иметь либо
        пустое значение - получить список всех питомцев, либо 'my_pets' - получить список собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        о добавлении нового питомца с фото."""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'Images/cat/jpg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}


        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result



    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        об удалении питомца по pet_id."""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def update_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        об изменении информации о питомце по pet_id."""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        о добавлении нового питомца без фото."""
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age,
            }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def set_photo(self, auth_key: json, pet_id: str, pet_photo: str):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
                о добавлении фото питомцу по pet_id."""
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result