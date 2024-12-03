import json
from pathlib import Path


class Observer:
    def update(self, items):
        pass


class Item:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = float(price)

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


class FilteredRepository:
    def __init__(self, repository, filter_condition=None):
        self.repository = repository
        self.filter_condition = filter_condition

    def set_filter(self, filter_condition):
        self.filter_condition = filter_condition

    def get_filtered_items(self):
        if self.filter_condition is None:
            return self.repository.get_all_items()
        return list(filter(self.filter_condition, self.repository.get_all_items()))

    def __getattr__(self, attr):
        return getattr(self.repository, attr)
