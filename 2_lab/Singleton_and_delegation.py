import mysql.connector

# Класс Database с применением паттерна Singleton
class Database:
    _instance = None

    def __new__(cls, host, user, password, database):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_db_connection(host, user, password, database)
        return cls._instance

    def _init_db_connection(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)  # Используем словарь для удобства

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor

    def commit(self):
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


# Класс MyEntity_rep_DB, использующий делегирование к Database
class MyEntity_rep_DB:
    def __init__(self, db):
        self.db = db  # Передаем экземпляр синглтона Database

    # a. Получить объект по ID
    def get_by_id(self, client_id):
        query = "SELECT * FROM Clients WHERE ClientID = %s"
        cursor = self.db.execute_query(query, (client_id,))
        return cursor.fetchone()

    # b. Получить список k по счету n объектов класса short
    def get_k_n_short_list(self, k, n):
        offset = (n - 1) * k
        query = "SELECT * FROM Clients LIMIT %s OFFSET %s"
        cursor = self.db.execute_query(query, (k, offset))
        return cursor.fetchall()

    # c. Добавить объект в список (при добавлении сформировать новый ID)
    def add_client(self, last_name, first_name, middle_name, address, phone):
        query = "INSERT INTO Clients (LastName, FirstName, MiddleName, Address, Phone) VALUES (%s, %s, %s, %s, %s)"
        self.db.execute_query(query, (last_name, first_name, middle_name, address, phone))
        self.db.commit()
        return self.db.cursor.lastrowid  # Возвращаем ID добавленного клиента

    # d. Заменить элемент списка по ID
    def update_client_by_id(self, client_id, last_name=None, first_name=None, middle_name=None, address=None, phone=None):
        client = self.get_by_id(client_id)
        if client:
            query = """
                UPDATE Clients 
                SET LastName = COALESCE(%s, LastName),
                    FirstName = COALESCE(%s, FirstName),
                    MiddleName = COALESCE(%s, MiddleName),
                    Address = COALESCE(%s, Address),
                    Phone = COALESCE(%s, Phone)
                WHERE ClientID = %s
            """
            self.db.execute_query(query, (last_name, first_name, middle_name, address, phone, client_id))
            self.db.commit()
            return True
        return False

    # e. Удалить элемент списка по ID
    def delete_client_by_id(self, client_id):
        query = "DELETE FROM Clients WHERE ClientID = %s"
        self.db.execute_query(query, (client_id,))
        self.db.commit()
        return self.db.cursor.rowcount > 0  # Возвращаем True, если удаление было успешным

    # f. Получить количество элементов
    def get_count(self):
        query = "SELECT COUNT(*) as count FROM Clients"
        cursor = self.db.execute_query(query)
        result = cursor.fetchone()
        return result['count']


# Пример использования:

# Инициализируем синглтон Database
db_singleton = Database(host='localhost', user='root', password='password', database='clients_db')

# Используем класс MyEntity_rep_DB с делегированием работы с БД через синглтон
db_entity = MyEntity_rep_DB(db=db_singleton)

# Добавление клиента
new_client_id = db_entity.add_client('Ivanov', 'Ivan', 'Ivanovich', 'Moscow', '+7-999-123-4567')
print(f"Добавлен клиент с ID {new_client_id}")

# Получение клиента по ID
client = db_entity.get_by_id(new_client_id)
print(client)

# Получение списка клиентов (например, вторые 20 клиентов)
clients_list = db_entity.get_k_n_short_list(20, 2)
print(clients_list)

# Обновление клиента
db_entity.update_client_by_id(new_client_id, last_name='Petrov')

# Удаление клиента
db_entity.delete_client_by_id(new_client_id)

# Получение количества клиентов
count = db_entity.get_count()
print(f"Количество клиентов: {count}")
