import yaml

# Сущность Client
class Client:
    def __init__(self, client_id, last_name, first_name, middle_name, address, phone):
        self.ClientID = client_id
        self.LastName = last_name
        self.FirstName = first_name
        self.MiddleName = middle_name
        self.Address = address
        self.Phone = phone

    def to_dict(self):
        return {
            "ClientID": self.ClientID,
            "LastName": self.LastName,
            "FirstName": self.FirstName,
            "MiddleName": self.MiddleName,
            "Address": self.Address,
            "Phone": self.Phone,
        }

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

class ClientRepYAML:
    def __init__(self, file_path):
        self.file_path = file_path
        self.clients = []
        self.load_data()

    # a. Чтение всех значений из файла
    def load_data(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or []
                self.clients = [Client.from_dict(item) for item in data]
        except FileNotFoundError:
            self.clients = []
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")

    # b. Запись всех значений в файл
    def save_data(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                yaml.dump([client.to_dict() for client in self.clients], file, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    # c. Получить объект по ID
    def get_by_id(self, client_id):
        for client in self.clients:
            if client.ClientID == client_id:
                return client
        return None

    # d. Получить k по счету n объектов
    def get_k_n_short_list(self, k, n):
        start = (k - 1) * n
        return self.clients[start: start + n]

    # e. Сортировать элементы по выбранному полю (фамилия)
    def sort_by_last_name(self):
        self.clients.sort(key=lambda client: client.LastName)

    # f. Добавить объект в список
    def add(self, client):
        client.ClientID = max([c.ClientID for c in self.clients], default=0) + 1
        self.clients.append(client)

    # g. Заменить элемент списка по ID
    def replace_by_id(self, client_id, updated_client):
        for i, client in enumerate(self.clients):
            if client.ClientID == client_id:
                self.clients[i] = updated_client
                return True
        return False

    # h. Удалить элемент списка по ID
    def delete_by_id(self, client_id):
        for i, client in enumerate(self.clients):
            if client.ClientID == client_id:
                del self.clients[i]
                return True
        return False

    # i. Получить количество элементов
    def get_count(self):
        return len(self.clients)

    # Показать все элементы
    def display_all(self):
        for client in self.clients:
            print(client.to_dict())

def main():
    file_path = "clients.yaml"
    repo = ClientRepYAML(file_path)

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
