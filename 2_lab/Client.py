import json
import os

class Client:
    def __init__(self, client_id, last_name, first_name, middle_name, address, phone):
        self.__client_id = client_id
        self.__last_name = last_name
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__address = address
        self.__phone = phone

    def get_client_id(self):
        return self.__client_id

    def set_client_id(self, client_id):
        self.__client_id = client_id

    def get_last_name(self):
        return self.__last_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_middle_name(self):
        return self.__middle_name

    def set_middle_name(self, middle_name):
        self.__middle_name = middle_name

    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address

    def get_phone(self):
        return self.__phone

    def set_phone(self, phone):
        self.__phone = phone

    def to_dict(self):
        return {
            "client_id": self.__client_id,
            "last_name": self.__last_name,
            "first_name": self.__first_name,
            "middle_name": self.__middle_name,
            "address": self.__address,
            "phone": self.__phone
        }

    @staticmethod
    def from_dict(data):
        return Client(
            data["client_id"],
            data["last_name"],
            data["first_name"],
            data["middle_name"],
            data["address"],
            data["phone"]
        )

class ShortClient:
    def __init__(self, first_name, last_name, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

class ClientRepJson:
    def __init__(self, filename):
        self.filename = filename
        self.clients = self.read_from_file()

    def read_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Client.from_dict(item) for item in data]
        return []

    def write_to_file(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([client.to_dict() for client in self.clients], file, indent=4)

    def get_client_by_id(self, client_id):
        for client in self.clients:
            if client.get_client_id() == client_id:
                return client
        return None

    def is_phone_unique(self, phone, exclude_client_id=None):
        for client in self.clients:
            if client.get_phone() == phone and client.get_client_id() != exclude_client_id:
                return False
        return True

    def get_k_n_short_list(self, k, n):
        start_index = (k - 1) * n
        end_index = start_index + n
        return [
            ShortClient(client.get_first_name(), client.get_last_name(), client.get_phone())
            for client in self.clients[start_index:end_index]
        ]

    def sort_by_field(self, field):
        self.clients.sort(key=lambda client: getattr(client, f"get_{field}")())

    def add_client(self, last_name, first_name, middle_name, address, phone):
        if not self.is_phone_unique(phone):
            print("Телефон уже используется другим клиентом.")
            return
        new_id = max([client.get_client_id() for client in self.clients], default=0) + 1
        new_client = Client(new_id, last_name, first_name, middle_name, address, phone)
        self.clients.append(new_client)
        self.write_to_file()

    def replace_client_by_id(self, client_id, last_name, first_name, middle_name, address, phone):
        if not self.is_phone_unique(phone, exclude_client_id=client_id):
            print("Телефон уже используется другим клиентом.")
            return False
        for i, client in enumerate(self.clients):
            if client.get_client_id() == client_id:
                self.clients[i] = Client(client_id, last_name, first_name, middle_name, address, phone)
                self.write_to_file()
                return True
        return False

    def delete_client_by_id(self, client_id):
        self.clients = [client for client in self.clients if client.get_client_id() != client_id]
        self.write_to_file()

    def get_count(self):
        return len(self.clients)

def main():
    client_rep = ClientRepJson("clients.json")

    while True:
        print("1. Показать всех клиентов")
        print("2. Добавить клиента")
        print("3. Найти клиента по ID")
        print("4. Заменить клиента по ID")
        print("5. Удалить клиента по ID")
        print("6. Получить количество клиентов")
        print("7. Сортировать клиентов по фамилии")
        print("8. Получить k по счету n объектов")
        print("0. Выход")

        choice = input("Выберите действие (0-8): ")

        if choice == "1":
            for client in client_rep.clients:
                print(client.to_dict())

        elif choice == "2":
            last_name = input("Введите фамилию: ")
            first_name = input("Введите имя: ")
            middle_name = input("Введите отчество: ")
            address = input("Введите адрес: ")
            phone = input("Введите телефон: ")
            client_rep.add_client(last_name, first_name, middle_name, address, phone)

        elif choice == "3":
            client_id = int(input("Введите ID клиента: "))
            client = client_rep.get_client_by_id(client_id)
            print(client.to_dict() if client else "Клиент не найден.")

        elif choice == "4":
            client_id = int(input("Введите ID клиента: "))
            last_name = input("Введите фамилию: ")
            first_name = input("Введите имя: ")
            middle_name = input("Введите отчество: ")
            address = input("Введите адрес: ")
            phone = input("Введите телефон: ")
            if not client_rep.replace_client_by_id(client_id, last_name, first_name, middle_name, address, phone):
                print("Клиент не найден или телефон уже используется.")

        elif choice == "5":
            client_id = int(input("Введите ID клиента: "))
            client_rep.delete_client_by_id(client_id)

        elif choice == "6":
            print(f"Количество клиентов: {client_rep.get_count()}")

        elif choice == "7":
            client_rep.sort_by_field("last_name")
            print("Сортировка выполнена.")

        elif choice == "8":
            k = int(input("Введите номер страницы (k): "))
            n = int(input("Введите количество элементов на странице (n): "))
            short_list = client_rep.get_k_n_short_list(k, n)
            for short_client in short_list:
                print(vars(short_client))

        elif choice == "0":
            break

        else:
            print("Некорректный выбор.")

if __name__ == "__main__":
    main()
