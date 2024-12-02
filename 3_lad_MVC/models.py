class Item:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class Repository:
    def __init__(self):
        self.items = []

    def get_all_items(self):
        return self.items

    def add_item(self, item):
        self.items.append(item)

    def update_item(self, id, new_item):
        for idx, item in enumerate(self.items):
            if item.id == id:
                self.items[idx] = new_item
                return True
        return False

    def delete_item(self, id):
        self.items = [item for item in self.items if item.id != id]
