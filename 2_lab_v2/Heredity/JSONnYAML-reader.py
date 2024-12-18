import json
import yaml
import os

# Базовый класс репозитория
class ClientRepositoryBase:
    def __init__(self, file_path):
        self.file_path = file_path
        self.clients = []
        self.load_data()

    # Загрузка данных (метод для переопределения)
    def load_data(self):
        raise NotImplementedError("Метод должен быть переопределен в подклассе")

    # Сохранение данных (метод для переопределения)
    def save_data(self):
        raise NotImplementedError("Метод должен быть переопределен в подклассе")

    # Получить объект по ID
    def get_by_id(self, client_id):
        return next((c for c in self.clients if c.ClientID == client_id), None)

    # Получить k по счету n объектов
    def get_k_n_short_list(self, k, n):
        start = (k - 1) * n
        return self.clients[start:start + n]

    # Сортировать элементы по фамилии
    def sort_by_last_name(self):
        self.clients.sort(key=lambda x: x.LastName)

    # Добавить объект
    def add(self, client):
        new_id = max((c.ClientID for c in self.clients), default=0) + 1
        client.ClientID = new_id
        self.clients.append(client)
        self.save_data()

    # Заменить элемент по ID
    def replace_by_id(self, client_id, updated_client):
        for index, client in enumerate(self.clients):
            if client.ClientID == client_id:
                updated_client.ClientID = client_id
                self.clients[index] = updated_client
                self.save_data()
                return True
        return False

    # Удалить элемент по ID
    def delete_by_id(self, client_id):
        client = self.get_by_id(client_id)
        if client:
            self.clients.remove(client)
            self.save_data()
            return True
        return False

    # Получить количество элементов
    def get_count(self):
        return len(self.clients)

    # Показать всех клиентов
    def display_all(self):
        for client in self.clients:
            print(
                f"ID: {client.ClientID}, {client.LastName} {client.FirstName}, Телефон: {client.Phone}"
            )

# Подкласс для работы с JSON
class ClientRepJSON(ClientRepositoryBase):
    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.clients = [Client.from_dict(item) for item in data]
        else:
            self.clients = []

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([client.to_dict() for client in self.clients], file, indent=4)

# Подкласс для работы с YAML
class ClientRepYAML(ClientRepositoryBase):
    def load_data(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or []
                self.clients = [Client.from_dict(item) for item in data]
        except FileNotFoundError:
            self.clients = []

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            yaml.dump(
                [client.to_dict() for client in self.clients],
                file,
                default_flow_style=False,
                allow_unicode=True,
            )

# Класс клиента
class Client:
    def __init__(self, ClientID, LastName, FirstName, MiddleName, Address, Phone):
        self.ClientID = ClientID
        self.LastName = LastName
        self.FirstName = FirstName
        self.MiddleName = MiddleName
        self.Address = Address
        self.Phone = Phone

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Client(
            data["ClientID"],
            data["LastName"],
            data["FirstName"],
            data["MiddleName"],
            data["Address"],
            data["Phone"],
        )

def main():
    file_type = input("Выберите формат файла (json/yaml): ").strip().lower()

    match file_type:
        case "json":
            repo = ClientRepJSON("clients.json")
        case "yaml":
            repo = ClientRepYAML("clients.yaml")
        case _:
            print("Неверный формат. Завершение программы.")
            return

    while True:
        print("\n1. Показать всех клиентов")
        print("2. Добавить клиента")
        print("3. Найти клиента по ID")
        print("4. Заменить клиента по ID")
        print("5. Удалить клиента по ID")
        print("6. Получить количество клиентов")
        print("7. Сортировать клиентов по фамилии")
        print("8. Получить k по счету n объектов")
        print("0. Выход")

        choice = input("Выберите опцию: ")

        match choice:
            case "1":
                repo.display_all()

            case "2":
                last_name = input("Фамилия: ")
                first_name = input("Имя: ")
                middle_name = input("Отчество: ")
                address = input("Адрес: ")
                phone = input("Телефон: ")
                new_client = Client(0, last_name, first_name, middle_name, address, phone)
                repo.add(new_client)
                print("Клиент добавлен.")

            case "3":
                client_id = int(input("Введите ID: "))
                client = repo.get_by_id(client_id)
                if client:
                    print(
                        f"ID: {client.ClientID}, {client.LastName} {client.FirstName}, Телефон: {client.Phone}"
                    )
                else:
                    print("Клиент не найден.")

            case "4":
                client_id = int(input("Введите ID для замены: "))
                last_name = input("Фамилия: ")
                first_name = input("Имя: ")
                middle_name = input("Отчество: ")
                address = input("Адрес: ")
                phone = input("Телефон: ")
                updated_client = Client(
                    0, last_name, first_name, middle_name, address, phone
                )
                if repo.replace_by_id(client_id, updated_client):
                    print("Клиент обновлен.")
                else:
                    print("Клиент не найден.")

            case "5":
                client_id = int(input("Введите ID для удаления: "))
                if repo.delete_by_id(client_id):
                    print("Клиент удален.")
                else:
                    print("Клиент не найден.")

            case "6":
                print(f"Количество клиентов: {repo.get_count()}")

            case "7":
                repo.sort_by_last_name()
                print("Сортировка выполнена.")

            case "8":
                k = int(input("Введите k (страница): "))
                n = int(input("Введите n (количество на странице): "))
                clients = repo.get_k_n_short_list(k, n)
                for client in clients:
                    print(
                        f"ID: {client.ClientID}, {client.LastName} {client.FirstName}, Телефон: {client.Phone}"
                    )

            case "0":
                print("Выход из программы.")
                break

            case _:
                print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
