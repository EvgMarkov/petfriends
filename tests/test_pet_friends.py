from settings import *
from api import APIRequest
import os

class TestPetFriends:
    def setup(self):
        self.pf = APIRequest()

    def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        status, result = self.pf.get_api_key(email, password)

        assert status == 200
        assert 'key' in result

    def test_get_list_of_pets_for_valid_key(self, filter=''):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)

        assert status == 200
        assert len(result['pets']) > 0

    def test_add_new_pet_with_valid_data(self, name='Катя', animal_type='сибирская',
                                         age='3', pet_photo='images/cat.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def test_successful_delete_self_pet(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) == 0:
            self.pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat.jpg")
            _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_id)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in my_pets.values()

    def test_successful_update_self_pet_info(self, name='Мурзик', animal_type='Кот', age=5):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")

    def test_get_api_key_for_invalid_password(self, email=valid_email, password=invalid_password):
        status, result = self.pf.get_api_key(email, password)

        assert status != 200

    def test_get_list_of_pets_with_filter(self, filter='my_pets'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)

        assert status == 200
        assert len(result['pets']) > 0

    def test_get_list_of_pets_for_invalid_filter(self, filter='hi'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)

        assert status != 200

    def test_create_pet_simple_with_valid_data(self, name='Мурзик', animal_type='кот',
                                               age='7'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.create_pet_simple(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    def test_create_pet_simple_with_invalid_data(self, name='Мурзик', animal_type='сиам',
                                                 age=''):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.create_pet_simple(auth_key, name, animal_type, age)
        assert status != 200

    def test_set_photo_with_valid_data(self, pet_photo='images/cat.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) == 0:
            self.pf.create_pet_simple(auth_key, "Кот", "кот", "3")
            _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = my_pets['pets'][0]['id']

        status, result = self.pf.set_photo(auth_key, pet_id, pet_photo)
        assert status == 200

    def test_create_pet_simple_with_long_name_in_data(self, name=invalid_data, animal_type='сиам',
                                                 age='5'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.create_pet_simple(auth_key, name, animal_type, age)
        assert status != 200

    def test_get_api_key_for_invalid_email(self, email=invalid_email, password=valid_password):
        status, result = self.pf.get_api_key(email, password)

        assert status != 200

    def test_create_pet_simple_with_long_anymal_type_in_data(self, name='Сиам', animal_type=invalid_data,
                                                 age='5'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.create_pet_simple(auth_key, name, animal_type, age)
        assert status != 200

    def test_unsuccessful_update_self_pet_info(self, name=invalid_data, animal_type='Котэ', age=5):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status != 200
        else:
            raise Exception("There is no my pets")