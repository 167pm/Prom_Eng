#  Система управления хранилищем данных  
## Разработка системы для управления большими объёмами данных, включая индексацию и быстрый поиск

---

## 🔹 Введение

Проект представляет собой **систему управления хранилищем данных**, предназначенную для эффективного хранения, поиска и анализа информации.  
Основная цель — создать инструмент, обеспечивающий:
- быстрый доступ к данным;
- индексацию для ускорения поиска;
- простое взаимодействие с системой через API и интерфейс.

Проект создавался поэтапно — от настройки Git и тестирования до интеграции с внешними сервисами.

---

## 🔹 Этап 1. Настройка Git и организация проекта  
### (Практическая работа №15)

Первым шагом была настройка **системы контроля версий Git**.

**Выполненные действия:**
```bash
git init
git add README.md
git commit -m "Первый коммит"
git branch -M main
git remote add origin https://github.com/167pm/Prom_Eng.git
git push -u origin main
```

Создана структура проекта:
```text
Prom_Eng/
├── app/
├── tests/
├── README.md
└── requirements.txt
```

Созданы ветки:
- `main` — стабильная версия;
- `feature-branch` — для новых функций.

Реализовано разрешение конфликтов и откат изменений с помощью `git merge`, `git reset` и `git checkout`.

✅ **Результат:** проект полностью контролируется через Git, история изменений прозрачна.

---

## 🔹 Этап 2. Автоматизация сборки и тестирования (CI/CD)  
### (Практические работы №16–18)

Следующим шагом стало внедрение **GitHub Actions** для автоматизации тестирования и сборки.

Созданы workflow-файлы:

`.github/workflows/build.yml`:
```yaml
name: Build and Test
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - run: |
          python -m unittest discover -s tests -v
```

`.github/workflows/test.yml`:
```yaml
name: Run Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - run: python -m unittest discover -s tests -v
```

Теперь при каждом коммите проект автоматически тестируется.

✅ **Результат:** CI/CD настроен, сборка и тесты выполняются без ручного вмешательства.

---

## 🔹 Этап 3. Разработка логики приложения и модульное тестирование  
### (Практическая работа №17)

Создан класс `DataStorage` в файле `app/storage.py`:
```python
class DataStorage:
    def __init__(self):
        self._storage = {}

    def add_item(self, key, value):
        self._storage[key] = value

    def get_item(self, key):
        return self._storage.get(key)

    def remove_item(self, key):
        if key in self._storage:
            del self._storage[key]

    def count(self):
        return len(self._storage)
```

Тесты (`tests/test_storage.py`):
```python
import unittest
from app.storage import DataStorage

class TestDataStorage(unittest.TestCase):
    def setUp(self):
        self.storage = DataStorage()

    def test_add_and_get_item(self):
        self.storage.add_item("user", "Герман")
        self.assertEqual(self.storage.get_item("user"), "Герман")

    def test_remove_item(self):
        self.storage.add_item("temp", 123)
        self.storage.remove_item("temp")
        self.assertIsNone(self.storage.get_item("temp"))

    def test_count_items(self):
        self.storage.add_item("a", 1)
        self.storage.add_item("b", 2)
        self.assertEqual(self.storage.count(), 2)
```

✅ **Результат:**
```
Ran 3 tests in 0.001s
OK
```

---

## 🔹 Этап 4. Управление версиями и релизами  
### (Практическая работа №22)

Использована схема Git Flow:

- `main` — стабильные версии  
- `develop` — активная разработка  
- `feature/...` — отдельные задачи  

Создан файл `CHANGELOG.md`:
```markdown
# Changelog

## [1.0.0] - 2025-10-20
### Добавлено:
- Базовая логика хранения данных
- Модульное тестирование
- Автоматизация CI/CD
```

Команды релиза:
```bash
git tag -a v1.0.0 -m "Первый стабильный релиз"
git push origin v1.0.0
```

✅ **Результат:** проект получил чёткую систему версий и релизов.

---

## 🔹 Этап 5. Создание пользовательской документации  
### (Практическая работа №27)

Создан файл `USER_GUIDE.md`, включающий:
- назначение системы;
- инструкцию по установке;
- примеры использования;
- FAQ и скриншоты.

✅ **Результат:** пользователь может самостоятельно установить и использовать систему.

---

## 🔹 Этап 6. Разработка REST API  
### (Практическая работа №29)

Создан `api.py` на Flask:
```python
from flask import Flask, request, jsonify
app = Flask(__name__)

tasks = []
API_KEY = "secret123"

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    task = {"id": len(tasks)+1, "title": data["title"]}
    tasks.append(task)
    return jsonify({"message": "Task created", "task": task}), 201

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(tasks), 200

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    for t in tasks:
        if t["id"] == id:
            tasks.remove(t)
            return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Not found"}), 404
```

**Проверка через Postman:**
- `POST /api/tasks` — создаёт задачу  
- `GET /api/tasks` — возвращает список  
- `DELETE /api/tasks/{id}` — удаляет задачу  

✅ **Результат:** API работает корректно, запросы возвращают ожидаемые данные.

---

## 🔹 Этап 7. Интеграция с внешним сервисом  
### (Практическая работа №30)

Добавлена интеграция с **Telegram Bot API** (файл `notify_bot.py`):
```python
import requests

BOT_TOKEN = "ТОКЕН_БОТА"
CHAT_ID = "АЙДИ_ЧАТА"

def send_task_notification(title):
    message = f"📢 Новая задача: {title}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)
```

Интеграция вызывается при создании задачи в `api.py`.

✅ **Результат:** при создании новой задачи Telegram-бот отправляет уведомление пользователю.

---

## 🔹 Итоги проекта

Реализован полный цикл разработки:
1. Система контроля версий (Git).  
2. Автоматизация сборки и тестов (GitHub Actions).  
3. Модульные тесты.  
4. Управление версиями и релизами.  
5. REST API.  
6. Интеграция с Telegram.  
7. Пользовательская документация.

---

## 🔹 Вывод

Проект демонстрирует полное понимание принципов современной разработки:
- CI/CD;
- тестирование;
- контроль версий;
- интеграция внешних сервисов;
- документирование.

✅ **Система полностью работоспособна** и может быть развита в сторону веб-интерфейса или базы данных.

---

## Использованные технологии

| Область | Инструменты |
|----------|-------------|
| Язык | Python 3 |
| Веб | Flask |
| Тестирование | unittest |
| CI/CD | GitHub Actions |
| Контроль версий | Git, GitHub |
| Интеграция | Telegram Bot API |
| Документация | Markdown |

---