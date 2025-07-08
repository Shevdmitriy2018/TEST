# 🧪 Тестовый проект: Авторизация

Автоматизированное тестирование страницы авторизации с использованием `pytest` и `selenium`.


## ⚙️ Используемые технологии

- Python 3.12
- Pytest 7.4.4 
- Selenium 4.21.0 
- Pytest-Sugar 

## 🚀 Как запустить тесты

Установи зависимости:
pip install -r requirements.txt

Запусти все тесты:
pytest -v

Позитивные и негативные тесты авторизации:
pytest -v authorization/test_login_positive_and_negative.py

Тесты авторизации по ссылкам:
pytest -v authorization/test_autorisations_links.py

