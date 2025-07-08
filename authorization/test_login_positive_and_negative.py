import os
import pytest
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
VALID_USERNAME = os.getenv("VALID_USERNAME")
VALID_PASSWORD = os.getenv("VALID_PASSWORD")


class Testlogin:
    @pytest.mark.login
    @pytest.mark.positive
    def test_valid_login(self, browser, logger):
        try:
            logger.info("✅ Зайти на сайт.")
            browser.get("https://stepik.org/")
            logger.info("✅ Кликнуть войти.")
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "navbar__auth_login"))
            ).click()
            logger.info("✅ Ввести логин.")
            login_input = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.NAME, "login"))
            )
            login_input.clear()
            login_input.send_keys(VALID_USERNAME)
            logger.info("✅ Ввести пароль.")
            password_input = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(VALID_PASSWORD)
            logger.info("✅ Кликнуть кнопку 'войти'.")
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "sign-form__btn"))
            ).click()
            profile_icon = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "navbar__profile-img"))
            )
            logger.info("✅Проверка авторизации.")
            assert profile_icon.is_displayed(), "Профиль не оттображается."
            logger.info(f"✅Авторизация успешна!")
        except AssertionError as ae:
            logger.error(f"❌ Авторизация не успешна! ошибка: {ae}")
            raise
        except Exception as e:
            logger.error(f"❌ ошибка при выполнении теста: {e}", exc_info=True)
            raise
        finally:
            logger.info("✅===Конец теста===")

    @pytest.mark.login
    @pytest.mark.negative
    @pytest.mark.parametrize("username, password, expected_error", [
        ("", "", "Заполните это поле."),
        ("", "ghj", "Заполните это поле."),
        ("Shevdmitriy@2018gmail.com", "", "Заполните это поле."),
        ("Shevdmitriy@2018gmail.com", "mlkn", "E-mail адрес и/или пароль не верны."),
    ])
    def test_login_validation_errors(self, username, password, expected_error, browser, logger):
        try:
            logger.info("✅ Зайти на сайт.")
            browser.get("https://stepik.org/")
            logger.info("✅ Кликнуть войти.")
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "navbar__auth_login"))
            ).click()
            logger.info("✅ Ввести логин.")
            login_input = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.NAME, "login"))
            )
            login_input.clear()
            login_input.send_keys(username)
            logger.info("✅ Ввести пароль.")
            password_input = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(password)
            logger.info("✅Нажать кнопку 'войти'.")
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "sign-form__btn"))
            ).click()
            if expected_error == "E-mail адрес и/или пароль не верны.":
                logger.info("✅Проверка сообщения авторизации.")
                error_message = WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//ul[@class='sign-form__messages']/li[@role='alert']"))
                ).text
                logger.info(f"❌Ожидали сообщение: '{expected_error}', вышло сообщение: '{error_message}'")
                assert expected_error.lower() in error_message.lower(), \
                    f"Ожидали увидеть: E-mail адрес и/или пароль не верны. Но вышло сообщение '{error_message}'"
            else:
                logger.info("✅Проверка валидации полей логина и пароля.")
                login_validation = browser.execute_script("return arguments[0].validationMessage;", login_input)
                password_validation = browser.execute_script("return arguments[0].validationMessage;", password_input)
                logger.info(
                    f"❌Ожидали сообщение: '{expected_error}', но получили: '{login_validation}' и '{password_validation}'")
                assert expected_error in (login_validation, password_validation), \
                    f"❌Ожидали: '{expected_error}', но получили '{login_validation}' и '{password_validation}'"
        except AssertionError as ae:
            logger.error(f"❌AssertionError: {ae}")
            raise
        except Exception as e:
            logger.error(f"❌Ошибка при выполнении теста: {e}", exc_info=True)
            raise
        finally:
            logger.info("✅===Конец теста===")
