import unittest
from app.storage import DataStorage

class TestDataStorage(unittest.TestCase):
    def setUp(self):
        """Подготавливает тестовую среду перед каждым тестом"""
        self.storage = DataStorage()

    def test_add_and_get_item(self):
        """Проверяет добавление и получение элемента"""
        self.storage.add_item("user", "Герман")
        self.assertEqual(self.storage.get_item("user"), "Герман")

    def test_remove_item(self):
        """Проверяет удаление элемента"""
        self.storage.add_item("temp", 123)
        self.storage.remove_item("temp")
        self.assertIsNone(self.storage.get_item("temp"))

    def test_count_items(self):
        """Проверяет количество элементов"""
        self.storage.add_item("a", 1)
        self.storage.add_item("b", 2)
        self.assertEqual(self.storage.count(), 2)

if __name__ == "__main__":
    unittest.main()
