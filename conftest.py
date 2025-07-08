# conftest.py
import os
import logging
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def credentials():
    load_dotenv()
    login = os.getenv("STEPIC_LOGIN")
    password = os.getenv("STEPIC_PASSWORD")
    assert login and password, "STEPIC_LOGIN или STEPIC_PASSWORD не заданы в .env!"
    return {"login": login, "password": password}


# Создаём папку logs, если её нет
os.makedirs("logs", exist_ok=True)

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Настройка логгера перед каждым тестом"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # ✅ Удаляем опасные символы
    import re
    safe_test_name = re.sub(r"[^\w\-_.]", "_", item.name)

    log_file = f"logs/{safe_test_name}_{timestamp}.log"

    logger = logging.getLogger("autotests")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info(f"=== НАЧАЛО ТЕСТА: {item.name} ===")


@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    """Очистка логгера после теста"""
    logger = logging.getLogger("autotests")
    logger.info(f"=== КОНЕЦ ТЕСТА: {item.name} ===")

    # Освобождаем хендлеры (иначе будут дублироваться)
    for handler in logger.handlers:
        handler.close()
    logger.handlers.clear()


@pytest.fixture(scope="session")
def logger():
    return logging.getLogger("autotests")

def pytest_addoption(parser):
    parser.addoption('--language', action='store', default=None,
                     help="Язык для запуска тестов (например, ru, en, de)")


@pytest.fixture(scope="function")
def browser(logger):
    user_language = "ru"

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--headless")  # если нужен режим без GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--lang={user_language}")
    options.add_experimental_option('prefs', {'intl.accept_languages': user_language})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.delete_all_cookies()
    logger.info(f"🚀 Запускаем браузер с языком: {user_language}, в режиме инкогнито.")
    logger.info("Очищены все cookies в браузере")

    yield driver

    logger.info("Закрываем браузер")
    driver.quit()
