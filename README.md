# 🧪 Тестовый проект: Авторизация

Автоматизированное тестирование страницы авторизации с использованием `pytest` и `selenium`.

## 📁 Структура проекта

├── test_login_positive_and_negative/
│ └── test_login_positive_and_negative.py # Тесты позитивного и негативного входа
├── test_autorisations_links/
│ └── test_autorisations_links.py # Тесты авторизации по ссылкам
├── requirements.txt # Зависимости проекта
├── README.md # Документация проекта
└── .gitignore # Исключения для Git

markdown
Копировать
Редактировать

## ⚙️ Используемые технологии

- Python 3.12
- Pytest 7.4.4 
- Selenium 4.21.0 
- Pytest-Sugar 

## 🚀 Как запустить тесты

1. Установи зависимости:

```bash
pip install -r requirements.txt
Запусти все тесты:

bash

pytest -v
Запуск конкретных тестов:

Позитивные и негативные тесты авторизации:

bash

pytest -v test_login_positive_and_negative/test_login_positive_and_negative.py
Тесты авторизации по ссылкам:

bash

pytest -v test_autorisations_links/test_autorisations_links.py
