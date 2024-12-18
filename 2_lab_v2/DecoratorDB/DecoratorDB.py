import mysql.connector
from abc import ABC, abstractmethod


# Базовый интерфейс репозитория
class IClientRepository(ABC):
    @abstractmethod
    def get_by_id(self, client_id: int):
        pass

    @abstractmethod
    def get_k_n_short_list(self, k: int, n: int):
        pass

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def replace_by_id(self, client_id: int, updated_entity):
        pass

    @abstractmethod
    def delete_by_id(self, client_id: int):
        pass

    @abstractmethod
    def get_count(self):
        pass


# Декоратор для репозитория
class ClientRepositoryDecorator(IClientRepository, ABC):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def get_by_id(self, client_id: int):
        return self._wrapped.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int):
        return self._wrapped.get_k_n_short_list(k, n)

    def add(self, entity):
        return self._wrapped.add(entity)

    def replace_by_id(self, client_id: int, updated_entity):
        return self._wrapped.replace_by_id(client_id, updated_entity)

    def delete_by_id(self, client_id: int):
        return self._wrapped.delete_by_id(client_id)

    def get_count(self):
        return self._wrapped.get_count()


# Декоратор для фильтрации
class FilterDecorator(ClientRepositoryDecorator):
    def __init__(self, wrapped, filter_conditions):
        super().__init__(wrapped)
        self.filter_conditions = filter_conditions

    def get_k_n_short_list(self, k: int, n: int):
        # Добавляем фильтрацию в SQL-запрос
        query = f"SELECT * FROM MyClient WHERE {self.filter_conditions} LIMIT %s OFFSET %s"
        return self._wrapped._execute_query(query, (n, (k - 1) * n))

    def get_count(self):
        # Добавляем фильтрацию в подсчет
        query = f"SELECT COUNT(*) AS Count FROM MyClient WHERE {self.filter_conditions}"
        result = self._wrapped._execute_query(query)
        return result[0]["Count"]


# Декоратор для сортировки
class SortDecorator(ClientRepositoryDecorator):
    def __init__(self, wrapped, sort_column, sort_order="ASC"):
        super().__init__(wrapped)
        self.sort_column = sort_column
        self.sort_order = sort_order

    def get_k_n_short_list(self, k: int, n: int):
        # Добавляем сортировку в SQL-запрос
        query = f"SELECT * FROM MyClient ORDER BY {self.sort_column} {self.sort_order} LIMIT %s OFFSET %s"
        return self._wrapped._execute_query(query, (n, (k - 1) * n))

    def get_count(self):
        # Добавляем сортировку в подсчет (если необходимо)
        query = f"SELECT COUNT(*) AS Count FROM MyClient"
        result = self._wrapped._execute_query(query)
        return result[0]["Count"]


# Класс для работы с базой данных
class MyClientRepDB:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def _execute_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def get_by_id(self, client_id):
        query = "SELECT * FROM MyClient WHERE ClientID = %s"
        result = self._execute_query(query, (client_id,))
        return MyClient.from_dict(result[0]) if result else None

    def get_k_n_short_list(self, k, n):
        query = "SELECT * FROM MyClient LIMIT %s OFFSET %s"
        results = self._execute_query(query, (n, (k - 1) * n))
        return [MyClient.from_dict(row) for row in results]

    def add(self, entity):
        query = "SELECT MAX(ClientID) AS MaxID FROM MyClient"
        max_id = self._execute_query(query)[0]["MaxID"] or 0
        new_id = max_id + 1
        query = "INSERT INTO MyClient (ClientID, LastName, FirstName, MiddleName, Address, Phone) VALUES (%s, %s, %s, %s, %s, %s)"
        self._execute_query(query, (new_id, entity.LastName, entity.FirstName, entity.MiddleName, entity.Address, entity.Phone))
        self.connection.commit()
        return new_id

    def replace_by_id(self, client_id, updated_entity):
        query = "UPDATE MyClient SET LastName = %s, FirstName = %s, MiddleName = %s, Address = %s, Phone = %s WHERE ClientID = %s"
        self._execute_query(query, (updated_entity.LastName, updated_entity.FirstName, updated_entity.MiddleName, updated_entity.Address, updated_entity.Phone, client_id))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_by_id(self, client_id):
        query = "DELETE FROM MyClient WHERE ClientID = %s"
        self._execute_query(query, (client_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def get_count(self):
        query = "SELECT COUNT(*) AS Count FROM MyClient"
        result = self._execute_query(query)
        return result[0]["Count"]
    
    def close(self):
        self.cursor.close()
        self.connection.close()


# Класс клиента
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


# Основная программа
def main():
    host = "localhost"
    user = "admin"
    password = "password"
    database = "testdb"

    repo = MyClientRepDB(host, user, password, database)

    # Ввод фильтра и сортировки
    filter_condition = input("Введите фильтрацию (например, 'LastName = \"Иванов\"'): ")
    sort_column = input("Введите столбец для сортировки: ")
    sort_order = input("Введите порядок сортировки (ASC/DESC): ").upper()

    # Применяем декораторы
    filtered_repo = FilterDecorator(repo, filter_condition) if filter_condition else repo
    sorted_repo = SortDecorator(filtered_repo, sort_column, sort_order)

    # Получение данных
    k = int(input("Введите номер страницы (k): "))
    n = int(input("Введите количество объектов на странице (n): "))
    clients = sorted_repo.get_k_n_short_list(k, n)
    print("Результаты поиска:")
    for client in clients:
        print(client.to_dict())

    count = sorted_repo.get_count()
    print(f"Общее количество записей: {count}")

    repo.close()


if __name__ == "__main__":
    main()
