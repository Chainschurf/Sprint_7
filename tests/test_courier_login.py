import pytest
import allure


@allure.suite("Courier Login Tests")
@allure.title("Test Courier Login")
class TestCourierLogin:

    @allure.step("Test login courier successfully")
    def test_login_courier_successfully(self, setup_and_teardown, login_courier):
        payload, response, courier_id = setup_and_teardown
        login_payload = {
            "login": payload['login'],
            "password": payload['password']
        }

        login_response = login_courier(login_payload)
        assert login_response.status_code == 200, "Expected status code 200 for successful login"

    @allure.step("Test login without login")
    def test_login_without_login(self, generate_user_data, login_courier):
        payload = {
            "password": generate_user_data['password']
        }
        response = login_courier(payload)
        assert response.json()['message'] == "Недостаточно данных для входа"

    @pytest.mark.xfailed
    @allure.step("Test login without password")
    def test_login_without_password(self, generate_user_data, login_courier):
        payload = {
            "login": generate_user_data['login']
        }
        response = login_courier(payload)
        assert response.json()['message'] == "Недостаточно данных для входа"

    @allure.step("Test login with invalid credentials")
    def test_login_with_invalid_credentials(self, login_courier):
        payload = {
            "login": "inv@/_idLogin",
            "password": "invalidPassword"
        }
        response = login_courier(payload)
        assert response.status_code == 404, "Expected status code 404 for incorrect login or password"

    @allure.step("Test login without one field")
    def test_login_without_one_field_error(self, generate_user_data, login_courier):
        payload = {
            "password": generate_user_data['password']
        }
        response = login_courier(payload)
        assert response.status_code == 400, "Expected status code 400 for missing field"

    @allure.step("Test login for nonexistent user")
    def test_login_for_nonexistent_user(self, login_courier):
        payload = {
            "login": "nonexistentUser",
            "password": "anyPassword"
        }
        response = login_courier(payload)
        assert response.status_code == 404, "Expected status code 404 for nonexistent user"

    @allure.step("Test successful login returns id")
    def test_successful_login_returns_id(self, setup_and_teardown, login_courier):
        payload, response, courier_id = setup_and_teardown
        login_payload = {
            "login": payload['login'],
            "password": payload['password']
        }

        login_response = login_courier(login_payload)
        assert 'id' in login_response.json(), "Response should contain courier ID"
