import json
from pathlib import Path


class Observer:
    """Интерфейс наблюдателя."""
    def update(self, items):
        pass


class Item:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"])


class Repository:
    def __init__(self, json_file="data.json"):
        self.json_file = Path(json_file)
        self.items = self._load_items()
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.items)

    def _load_items(self):
        if self.json_file.exists():
            with open(self.json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Item.from_dict(item) for item in data]
        return []

    def _save_items(self):
        with open(self.json_file, "w", encoding="utf-8") as file:
            json.dump([item.to_dict() for item in self.items], file, indent=4, ensure_ascii=False)

    def get_all_items(self):
        return self.items

    def add_item(self, item):
        self.items.append(item)
        self._save_items()
        self.notify_observers()

    def update_item(self, id, new_item):
        for idx, item in enumerate(self.items):
            if item.id == id:
                self.items[idx] = new_item
                self._save_items()
                self.notify_observers()
                return True
        return False

    def delete_item(self, id):
        self.items = [item for item in self.items if item.id != id]
        self._save_items()
        self.notify_observers()

    def filter_items(self, condition):
        return list(filter(condition, self.items))

    def sort_items(self, key, reverse=False):
        self.items.sort(key=key, reverse=reverse)
        self._save_items()
        self.notify_observers()
