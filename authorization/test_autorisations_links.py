import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import math
from selenium.common.exceptions import TimeoutException


class Test:
    def calc(self):
        return str(math.log(int(time.time())))

    @pytest.mark.parametrize("link",

                             [
                                 "https://stepik.org/lesson/236895/step/1",
                                 "https://stepik.org/lesson/236896/step/1",
                                 "https://stepik.org/lesson/236897/step/1",
                                 "https://stepik.org/lesson/236898/step/1",
                                 "https://stepik.org/lesson/236899/step/1",
                                 "https://stepik.org/lesson/236903/step/1",
                                 "https://stepik.org/lesson/236904/step/1",
                                 "https://stepik.org/lesson/236905/step/1"
                             ])
    def test_authorization(self, browser, logger, credentials, link):
        logger.info("Шаг 1. Открываем страницу!")

        browser.get(link)

        logger.info("Шаг 2. Ищем кнопку для входа и кликаем")
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "navbar__auth_login"))
        ).click()

        logger.info("Шаг 3. Вводим логин и пароль.")
        browser.find_element(By.NAME, "login").send_keys(credentials["login"])
        browser.find_element(By.NAME, "password").send_keys(credentials["password"])

        logger.info("Шаг 4. Кликаем на кнопку входа.")
        browser.find_element(By.CLASS_NAME, "sign-form__btn").click()

        logger.info("Шаг 5. Ждем, пока форма входа исчезнет.")
        WebDriverWait(browser, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "sign-form__btn"))
        )
        answer = self.calc()
        logger.info("Шаг 6. Ждем активную кнопку обновления и кликаем.")
        try:
            again_btn = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Решить снова']"))
            )
            again_btn.click()
            logger.info("Кнопка 'решить снова' найдена.")
        except TimeoutException:
            logger.info("Шаг 7. Вводим текст в поле ответа.")
        text_area = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ember-text-area"))
        )
        text_area.clear()
        text_area.send_keys(answer)
        logger.info("Шаг 8. Жмем кнопку отправки.")
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "submit-submission"))
        ).click()
        hint = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "smart-hints"))
        )
        ls = []
        result_text = hint.text
        if result_text != "Correct!":
            ls.append(result_text)
        if ls:
            logger.error(f"ошибки в тесте {link}: {ls}")
            logger.info(f"тест прошел успешно {link}")
        assert not ls, f"ошибки в тесте {ls}"

