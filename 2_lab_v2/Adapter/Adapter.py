import mysql.connector
from abc import ABC, abstractmethod

# Класс MyClient
class MyClient:
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
            "Phone": self.Phone
        }

    @staticmethod
    def from_dict(data):
        return MyClient(
            data["ClientID"],
            data["LastName"],
            data["FirstName"],
            data["MiddleName"],
            data["Address"],
            data["Phone"]
        )


# Интерфейс репозитория
class IClientRepository(ABC):
    @abstractmethod
    def get_by_id(self, client_id):
        pass

    @abstractmethod
    def get_k_n_short_list(self, k, n):
        pass

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def replace_by_id(self, client_id, updated_entity):
        pass

    @abstractmethod
    def delete_by_id(self, client_id):
        pass

    @abstractmethod
    def get_count(self):
        pass


# Класс для работы с базой данных MySQL
class MyClientRepDB:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def get_by_id(self, client_id):
        query = "SELECT * FROM MyClient WHERE ClientID = %s"
        self.cursor.execute(query, (client_id,))
        result = self.cursor.fetchone()
        return MyClient.from_dict(result) if result else None

    def get_k_n_short_list(self, k, n):
        offset = (k - 1) * n
        query = "SELECT * FROM MyClient LIMIT %s OFFSET %s"
        self.cursor.execute(query, (n, offset))
        results = self.cursor.fetchall()
        return [MyClient.from_dict(row) for row in results]

    def add(self, entity):
        query = "SELECT MAX(ClientID) AS MaxID FROM MyClient"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()["MaxID"] or 0
        new_id = max_id + 1

        query = "INSERT INTO MyClient (ClientID, LastName, FirstName, MiddleName, Address, Phone) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (new_id, entity.LastName, entity.FirstName, entity.MiddleName, entity.Address, entity.Phone))
        self.connection.commit()
        entity.ClientID = new_id
        return new_id

    def replace_by_id(self, client_id, updated_entity):
        query = """
            UPDATE MyClient
            SET LastName = %s, FirstName = %s, MiddleName = %s, Address = %s, Phone = %s
            WHERE ClientID = %s
        """
        self.cursor.execute(
            query, (updated_entity.LastName, updated_entity.FirstName, updated_entity.MiddleName, updated_entity.Address, updated_entity.Phone, client_id)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_by_id(self, client_id):
        query = "DELETE FROM MyClient WHERE ClientID = %s"
        self.cursor.execute(query, (client_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def get_count(self):
        query = "SELECT COUNT(*) AS Count FROM MyClient"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result["Count"]

    def close(self):
        self.cursor.close()
        self.connection.close()


# Адаптер для работы с базой данных
class MyClientRepDBAdapter(IClientRepository):
    def __init__(self, host, user, password, database):
        self.repo = MyClientRepDB(host, user, password, database)

    def get_by_id(self, client_id):
        return self.repo.get_by_id(client_id)

    def get_k_n_short_list(self, k, n):
        return self.repo.get_k_n_short_list(k, n)

    def add(self, entity):
        return self.repo.add(entity)

    def replace_by_id(self, client_id, updated_entity):
        return self.repo.replace_by_id(client_id, updated_entity)

    def delete_by_id(self, client_id):
        return self.repo.delete_by_id(client_id)

    def get_count(self):
        return self.repo.get_count()


# Главная программа
def main():
    host = "localhost"
    user = "admin"
    password = "password"
    database = "testdb"

    # Создаем адаптер для работы с базой данных
    repo = MyClientRepDBAdapter(host, user, password, database)

    def get_object_by_id():
        client_id = int(input("Введите ID объекта: "))
        entity = repo.get_by_id(client_id)
        if entity:
            print("Объект:", entity.to_dict())
        else:
            print("Объект не найден.")

    def get_k_n_list():
        k = int(input("Введите номер страницы (k): "))
        n = int(input("Введите количество объектов на странице (n): "))
        entities = repo.get_k_n_short_list(k, n)
        if entities:
            for entity in entities:
                print(entity.to_dict())
        else:
            print("Записи не найдены.")

    def add_object():
        last_name = input("Введите фамилию: ")
        first_name = input("Введите имя: ")
        middle_name = input("Введите отчество: ")
        address = input("Введите адрес: ")
        phone = input("Введите телефон: ")
        new_entity = MyClient(0, last_name, first_name, middle_name, address, phone)
        new_id = repo.add(new_entity)
        print(f"Добавлен объект с ID: {new_id}")

    def replace_object():
        client_id = int(input("Введите ID объекта для обновления: "))
        last_name = input("Введите новую фамилию: ")
        first_name = input("Введите новое имя: ")
        middle_name = input("Введите новое отчество: ")
        address = input("Введите новый адрес: ")
        phone = input("Введите новый телефон: ")
        updated_entity = MyClient(0, last_name, first_name, middle_name, address, phone)
        if repo.replace_by_id(client_id, updated_entity):
            print("Объект обновлен.")
        else:
            print("Ошибка обновления.")

    def delete_object():
        client_id = int(input("Введите ID объекта для удаления: "))
        if repo.delete_by_id(client_id):
            print("Объект удален.")
        else:
            print("Ошибка удаления.")

    def get_count():
        print("Общее количество записей:", repo.get_count())

    actions = {
        "1": get_object_by_id,
        "2": get_k_n_list,
        "3": add_object,
        "4": replace_object,
        "5": delete_object,
        "6": get_count,
        "7": lambda: print("Выход из программы.")
    }

    while True:
        print("\nМеню:")
        print("1. Получить объект по ID")
        print("2. Получить список объектов (k по счету n)")
        print("3. Добавить объект")
        print("4. Заменить объект по ID")
        print("5. Удалить объект по ID")
        print("6. Получить количество элементов")
        print("7. Выход")

        choice = input("Выберите опцию: ")

        action = actions.get(choice)
        if action:
            action()
            if choice == "7":
                break
        else:
            print("Неверный выбор, попробуйте снова.")

    repo.repo.close()


if __name__ == "__main__":
    main()
