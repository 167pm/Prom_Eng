# Модуль хранения данных

class DataStorage:
    def __init__(self):
        self._storage = {}

    def add_item(self, key, value):
        """Добавляет элемент в хранилище"""
        self._storage[key] = value

    def get_item(self, key):
        """Возвращает элемент по ключу"""
        return self._storage.get(key)

    def remove_item(self, key):
        """Удаляет элемент, если он существует"""
        if key in self._storage:
            del self._storage[key]

    def count(self):
        """Возвращает количество элементов"""
        return len(self._storage)
