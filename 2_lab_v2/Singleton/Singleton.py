import mysql.connector


class DatabaseConnection:
    _instance = None

    # Паттерн одиночка: гарантирует, что будет только одно подключение к базе данных
    def __new__(cls, host, user, password, database):
        # Если экземпляр еще не создан, создаем его
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            # Устанавливаем подключение к базе данных
            cls._instance.connection = mysql.connector.connect(
                host=host, user=user, password=password, database=database
            )
            cls._instance.cursor = cls._instance.connection.cursor(dictionary=True)
        return cls._instance

    # Возвращает подключение к базе данных
    def get_connection(self):
        return self.connection

    # Возвращает курсор для выполнения запросов
    def get_cursor(self):
        return self.cursor

    # Закрывает соединение с базой данных
    def close(self):
        self.cursor.close()
        self.connection.close()


class MyClient:
    def __init__(self, client_id, last_name, first_name, middle_name, address, phone):
        self.ClientID = client_id
        self.LastName = last_name
        self.FirstName = first_name
        self.MiddleName = middle_name
        self.Address = address
        self.Phone = phone

    # Преобразует объект MyClient в словарь для удобства работы с данными
    def to_dict(self):
        return {
            "ClientID": self.ClientID,
            "LastName": self.LastName,
            "FirstName": self.FirstName,
            "MiddleName": self.MiddleName,
            "Address": self.Address,
            "Phone": self.Phone
        }

    # Статический метод для создания объекта MyClient из словаря
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


class MyClientRepDB:
    def __init__(self, host, user, password, database):
        # Используем паттерн одиночка для подключения
        db_connection = DatabaseConnection(host, user, password, database)
        self.connection = db_connection.get_connection()
        self.cursor = db_connection.get_cursor()

    # a. Получить объект по ID
    def get_by_id(self, client_id):
        query = "SELECT * FROM MyClient WHERE ClientID = %s"
        self.cursor.execute(query, (client_id,))
        result = self.cursor.fetchone()
        return MyClient.from_dict(result) if result else None

    # b. Получить список k по счету n объектов (с пагинацией)
    def get_k_n_short_list(self, k, n):
        offset = (k - 1) * n
        query = "SELECT * FROM MyClient LIMIT %s OFFSET %s"
        self.cursor.execute(query, (n, offset))
        results = self.cursor.fetchall()
        return [MyClient.from_dict(row) for row in results]

    # c. Добавить объект в базу данных
    def add(self, entity):
        # Определение нового ID для добавляемого клиента
        query = "SELECT MAX(ClientID) AS MaxID FROM MyClient"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()["MaxID"] or 0
        new_id = max_id + 1

        # Добавление объекта в базу данных
        query = "INSERT INTO MyClient (ClientID, LastName, FirstName, MiddleName, Address, Phone) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (new_id, entity.LastName, entity.FirstName, entity.MiddleName, entity.Address, entity.Phone))
        self.connection.commit()
        entity.ClientID = new_id
        return new_id

    # d. Заменить объект по ID
    def replace_by_id(self, client_id, updated_entity):
        query = """
            UPDATE MyClient
            SET LastName = %s, FirstName = %s, MiddleName = %s, Address = %s, Phone = %s
            WHERE ClientID = %s
        """
        self.cursor.execute(
            query, (updated_entity.LastName, updated_entity.FirstName, updated_entity.MiddleName, updated_entity.Address, updated_entity.Phone, client_id)
        )
        self.connection.commit()  # Подтверждаем изменения
        return self.cursor.rowcount > 0  # Возвращаем True, если строка была обновлена

    # e. Удалить объект по ID
    def delete_by_id(self, client_id):
        query = "DELETE FROM MyClient WHERE ClientID = %s"
        self.cursor.execute(query, (client_id,))
        self.connection.commit()  # Подтверждаем удаление
        return self.cursor.rowcount > 0  # Возвращаем True, если строка была удалена

    # f. Получить количество объектов в базе данных
    def get_count(self):
        query = "SELECT COUNT(*) AS Count FROM MyClient"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result["Count"]

    # Закрыть соединение с базой данных
    def close(self):
        self.cursor.close()
        self.connection.close()


def main():
    host = "localhost"
    user = "admin"
    password = "password"
    database = "testdb"

    repo = MyClientRepDB(host, user, password, database)

    # Функция для получения объекта по ID
    def get_object_by_id():
        client_id = int(input("Введите ID объекта: "))
        entity = repo.get_by_id(client_id)
        if entity:
            print("Объект:", entity.to_dict())
        else:
            print("Объект не найден.")

    # Функция для получения списка объектов с пагинацией
    def get_k_n_list():
        k = int(input("Введите номер страницы (k): "))
        n = int(input("Введите количество объектов на странице (n): "))
        entities = repo.get_k_n_short_list(k, n)
        if entities:
            for entity in entities:
                print(entity.to_dict())
        else:
            print("Записи не найдены.")

    # Функция для добавления нового объекта
    def add_object():
        last_name = input("Введите фамилию: ")
        first_name = input("Введите имя: ")
        middle_name = input("Введите отчество: ")
        address = input("Введите адрес: ")
        phone = input("Введите телефон: ")
        new_entity = MyClient(0, last_name, first_name, middle_name, address, phone)
        new_id = repo.add(new_entity)
        print(f"Добавлен объект с ID: {new_id}")

    # Функция для замены объекта по ID
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

    # Функция для удаления объекта по ID
    def delete_object():
        client_id = int(input("Введите ID объекта для удаления: "))
        if repo.delete_by_id(client_id):
            print("Объект удален.")
        else:
            print("Ошибка удаления.")

    # Функция для получения количества объектов
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

    repo.close()


if __name__ == "__main__":
    main()
