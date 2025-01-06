from dataclasses import field

import yaml
import json
import psycopg2
import os

class DatabaseConnector:
    __instance = None

    @staticmethod
    def get_instance(host, user, password, database, port=5432):
        if DatabaseConnector.__instance is None:
            DatabaseConnector(host, user, password, database, port)
        return DatabaseConnector.__instance

    def __init__(self, host, user, password, database, port=5432):
        if DatabaseConnector.__instance is not None:
            raise Exception("Это паттерн 'Одиночка'")
        else:
            DatabaseConnector.__instance = self
            self.connection = None
            self.cursor = None
            try:
                self.connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=port
                )
                self.cursor = self.connection.cursor()
            except psycopg2.Error as e:
                print(f"Ошибка подключения к базе данных PostgreSQL: {e}")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor
        except psycopg2.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()


class ClientDB:
    def __init__(self, host, user, password, database, port=5432):
        self.db_connector = db_connector

    def initialize_db(self):
        cursor = self.db_connector.execute_query("""
            CREATE TABLE IF NOT EXISTS Client (
                ClientID SERIAL PRIMARY KEY,
                LastName VARCHAR(255) NOT NULL,
                FirstName VARCHAR(255) NOT NULL,
                MiddleName VARCHAR(255) NOT NULL,
                Address TEXT NOT NULL,
                Phone VARCHAR(20) NOT NULL
            )
        """)
        if cursor:
            print("База данных PostgreSQL и таблица 'Client' успешно созданы.")

    def get_client_by_id(self, client_id):
        cursor = self.db_connector.execute_query("SELECT * FROM Client WHERE ClientID = %s", (client_id,))
        if cursor:
            result = cursor.fetchone()
            return dict(zip([desc[0] for desc in cursor.description], result)) if result else None
        return None

    def get_all_client(self):
        cursor = self.db_connector.execute_query("SELECT * FROM Client")
        if cursor:
            results = cursor.fetchall()
            return [dict(zip([desc[0] for desc in cursor.description], row)) for row in results]
        return []

    def add_client(self, client_data):
        query = """INSERT INTO Client (LastName, FirstName, MiddleName, Address, Phone) 
                    VALUES (%s, %s, %s, %s, %s) RETURNING ClientID;"""
        cursor = self.db_connector.execute_query(query, (client_data['LastName'],
                                                         client_data['FirstName'],
                                                         client_data['MiddleName'],
                                                         client_data['Address'],
                                                         client_data['Phone']))
        if cursor:
            result = cursor.fetchone()
            return result[0] if result else None
        return None

    def update_client(self, client_id, updated_client):
        query = """UPDATE Client
                    SET LastName = %s, FirstName = %s, MiddleName = %s, Address = %s, Phone = %s
                    WHERE ClientID = %s"""
        self.cursor.execute(query, (updated_client['LastName'],
                                    updated_client['FirstName'],
                                    updated_client['MiddleName'],
                                    updated_client['Address'],
                                    updated_client['Phone'],
                                    client_id))
        print("Данные клиента успешно обновлены.")

    def delete_client(self, client_id):
        cursor = self.db_connector.execute_query("DELETE FROM Client WHERE ClientID = %s", (client_id,))
        return cursor is not None

    def get_count(self):
        cursor = self.db_connector.execute_query("SELECT COUNT(*) FROM Client")
        if cursor:
            result = cursor.fetchone()
            return result[0] if result else 0
        return 0

    def get_k_n_short_list(self, k, n):
        offset = (k - 1) * n
        cursor = self.db_connector.execute_query("SELECT LastName, FirstName, MiddleName, Address, Phone FROM Client LIMIT %s OFFSET %s", (n, offset))
        if cursor:
            results = cursor.fetchall()
            return [dict(zip(['LastName', 'FirstName', 'MiddleName', 'Address', 'Phone'], row)) for row in results]
        return []


class Client:
    @staticmethod
    def validate_field(field_name, field_value, expected_type):
        if not isinstance(field_value, expected_type):
            raise ValueError(f"{field_name} должен быть типа {expected_type.__name__}.")
        if expected_type == str and not field_value.strip():
            raise ValueError(f"{field_name} не может быть пустым.")

    def __init__(self, *args):
        if len(args) == 6:
            client_id, last_name, first_name, middle_name, address, phone = args
            self._validate_and_set(client_id, last_name, first_name, middle_name, address, phone)
        elif len(args) == 1 and isinstance(args[0], str):
            self._from_json(args[0])
        elif len(args) == 1 and isinstance(args[0], Client):
            self._from_client(args[0])
        else:
            raise ValueError("Неверные аргументы для конструктора.")

    def _validate_and_set(self, client_id, last_name, first_name, middle_name, address, phone):
        Client.validate_field("ClientID", client_id, int)
        Client.validate_field("Фамилия", last_name, str)
        Client.validate_field("Имя", first_name, str)
        Client.validate_field("Отчество", middle_name, str)
        Client.validate_field("Адрес", address, str)
        Client.validate_field("Телефон", phone, str)

        self._client_id = client_id
        self._last_name = last_name
        self._first_name = first_name
        self._middle_name = middle_name
        self._address = address
        self._phone = phone

    def _from_json(self, json_string):
        try:
            data = json.loads(json_string)
            client_id = int(data['ID'])
            last_name = data['Фамилия']
            first_name = data['Имя']
            middle_name = data['Отчество']
            address = data['Адрес']
            phone = data['Телефон']
            self._validate_and_set(client_id, last_name, first_name, middle_name, address, phone)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Ошибка при разборе JSON: {e}")

    def _from_yaml(self, yaml_string):
        try:
            data = yaml.safe_load(yaml_string)
            client_id = int(data['ID'])
            last_name = data['Фамилия']
            first_name = data['Имя']
            middle_name = data['Отчество']
            address = data['Адрес']
            phone = data['Телефон']
            self._validate_and_set(client_id, last_name, first_name, middle_name, address, phone)
        except (yaml.YAMLError, KeyError, ValueError) as e:
            raise ValueError(f"Ошибка при разборе yaml: {e}")

    def _from_client(self, client):
        self._client_id = client._client_id
        self._last_name = client._last_name
        self._first_name = client._first_name
        self._middle_name = client._middle_name
        self._address = client._address
        self._phone = client._phone

    def __str__(self):
        return (f"Client(ID={self._client_id}, Фамилия='{self._last_name}', "
                f"Имя='{self._first_name}', Отчество='{self._middle_name}', "
                f"Адрес='{self._address}', Телефон='{self._phone}')")

    def __repr__(self):
        return f"Client(ID={self._client_id}, Фамилия='{self._last_name}')"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return self._client_id == other._client_id

    def get_short(self):
        return ClientShort(self)


class ClientShort:
    def __init__(self, client):
        if not isinstance(client, Client):
            raise ValueError("Параметр должен быть экземпляром класса Client.")
        self._client = client

    def __str__(self):
        return (f"ClientShort(ID={self._client._client_id}, "
                f"Фамилия={self._client._last_name}, Телефон={self._client._phone})")


class Client_rep:
    def __init__(self, filepath):
        self.filepath = filepath
        self.clients = []
        self.next_id = 1
        if os.path.exists(self.filepath):
            self.load_data()

    def get_client_by_id(self, client_id):
        for client in self.clients:
            if client._client_id == client_id:
                return client
        return None

    def get_k_n_short_list(self, k, n):
        return [str(ClientShort(c)) for c in self.clients[(k - 1) * n:(k - 1) * n + n]]

    def sort_by_field(self, field):
        try:
            self.clients.sort(key=lambda x: getattr(x, f"_{field}"))
        except AttributeError:
            print(f"Поле '{field}' не найдено.")

    def add_client(self, last_name, first_name, middle_name, address, phone):
        new_client = Client(self.next_id, last_name, first_name, middle_name, address, phone)
        self.clients.append(new_client)
        self.next_id += 1
        self.save_data()
        return new_client

    def update_client(self, client_id, last_name, first_name, middle_name, address, phone):
        client = self.get_client_by_id(client_id)
        if client:
            client._last_name = last_name
            client._first_name = first_name
            client._middle_name = middle_name
            client._address = address
            client._phone = phone
            self.save_to_yaml()
            return True
        return False

    def delete_client(self, client_id):
        self.clients = [c for c in self.clients if c._client_id != client_id]
        self.save_data()

    def get_count(self):
        return len(self.clients)


class Client_rep_yaml(Client_rep):
    def __init__(self, filepath="clients.yaml"):
        super().__init__(filepath)

    def load_data(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data:
                    for client_data in data:
                        self.clients.append(Client(*client_data.values()))
                    self.next_id = max(c._client_id for c in self.clients) + 1 if self.clients else 1
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Ошибка при загрузке из YAML: {e}")

    def save_data(self):
        try:
            data = [vars(c) for c in self.clients]
            with open(self.filepath, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Ошибка при сохранении в YAML: {e}")


class Client_rep_json(Client_rep):
    def __init__(self, filepath="clients.json"):
        super().__init__(filepath)

    def load_data(self):
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                for item in data:
                    self.clients.append(Client(*item.values()))
                self.next_id = max(c._client_id for c in self.clients) + 1 if self.clients else 1
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке из JSON: {e}")

    def save_data(self):
        try:
            data = [vars(c) for c in self.clients]
            with open(self.filepath, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при сохранении в JSON: {e}")


def run_operations(client_rep):
    clients = client_rep.get_all_client()
    while True:
        print("\nМеню:")
        print("1. Вывести всех клиентов")
        print("2. Добавить клиента")
        print("3. Удалить клиента")
        print("4. Изменить данные клиента")
        print("5. Найти клиента по ID")
        print("6. Получить k-n короткий список")
        print("7. Отсортировать клиентов")
        print("8. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                print("\nВсе клиенты:")
                for client in clients:
                    print(client)
            elif choice == "2":
                client_data = {
                    'LastName': input("Введите фамилию: "),
                    'FirstName': input("Введите имя: "),
                    'MiddleName': input("Введите отчество: "),
                    'Address': input("Введите адрес: "),
                    'Phone': input("Введите телефон: ")
                }
                if client_rep.add_client(client_data):
                    clients = client_rep.get_all_client()
                    print("Клиент добавлен")
                else:
                    print("Ошибка при добавлении клиента")
            elif choice == "3":
                client_id = int(input("Введите ID клиента для удаления: "))
                if client_rep.delete_client(client_id):
                    clients = client_rep.get_all_client()
                    print("Клиент удален")
                else:
                    print("Клиент не найден или ошибка при удалении")
            elif choice == "4":
                client_id = int(input("Введите ID клиента для изменения: "))
                client = client_rep.get_client_by_id(client_id)
                if client:
                    updated_client = {
                        'LastName': input(f"Новая фамилия ({client['LastName']}): ") or client['LastName'],
                        'FirstName': input(f"Новое имя ({client['FirstName']}): ") or client['FirstName'],
                        'MiddleName': input(f"Новое отчество ({client['MiddleName']}): ") or client['MiddleName'],
                        'Address': input(f"Новый адрес ({client['Address']}): ") or client['Address'],
                        'Phone': input(f"Новый телефон ({client['Phone']}): ") or client['Phone']
                    }
                    client_rep.update_client(client_id, updated_client)
                    clients = client_rep.get_all_client()
                    print("Данные клиента изменены")
                else:
                    print("Клиент не найден")
            elif choice == "5":
                client_id = int(input("Введите ID клиента: "))
                client = client_rep.get_client_by_id(client_id)
                if client:
                    print("\nНайденный клиент:", client)
                else:
                    print("Клиент не найден.")
            elif choice == "6":
                k = int(input("Введите номер страницы (k): "))
                n = int(input("Введите количество клиентов на странице (n): "))
                short_list = client_rep.get_k_n_short_list(k, n)
                print("\nКраткая информация о клиентах:", short_list)
            elif choice == "7":
                count = client_rep.get_count()
                print(f"Количество клиентов: {count}")
            elif choice == "8":
                print("Выход")
                break
            else:
                print("Неверный выбор")
        except ValueError:
            print("Неверный формат ввода. Пожалуйста, введите число.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def main():
    host = 'localhost'
    user = 'postgres'
    password = 'dimal'
    database = 'LiksDB'

    client_rep = None
    try:
        client_rep = ClientDB(host, user, password, database)
        client_rep.initialize_db()
        run_operations(client_rep)
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
    finally:
        if client_rep:
            client_rep.close()
            print("Соединение с базой данных закрыто.")


"""
def main():
    while True:
        print("\nМеню:")
        print("1. Выбрать JSON")
        print("2. Выбрать YAML")
        print("3. Выход")

        choice = input("Выберите тип файла: ")

        if choice == "1":
            client_rep = Client_rep_json()
            run_operations(client_rep)
        elif choice == "2":
            client_rep = Client_rep_yaml()
            run_operations(client_rep)
        elif choice == "3":
            print("Выход")
            break
        else:
            print("Неверный выбор.")

def run_operations(client_rep):
    while True:
        print("\nМеню:")
        print("1. Вывести всех клиентов")
        print("2. Добавить клиента")
        print("3. Удалить клиента")
        print("4. Изменить данные клиента")
        print("5. Найти клиента по ID")
        print("6. Получить k-n короткий список")
        print("7. Отсортировать клиентов")
        print("8. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                print("\nВсе клиенты:")
                for client in client_rep.clients:
                    print(client)

            elif choice == "2":
                last_name = input("Введите фамилию: ")
                first_name = input("Введите имя: ")
                middle_name = input("Введите отчество: ")
                address = input("Введите адрес: ")
                phone = input("Введите телефон: ")
                client_rep.add_client(last_name, first_name, middle_name, address, phone)
                print("Клиент добавлен")

            elif choice == "3":
                client_id = int(input("Введите ID клиента для удаления: "))
                client_rep.delete_client(client_id)
                print("Клиент удален")

            elif choice == "4":
                client_id = int(input("Введите ID клиента для изменения: "))
                client = client_rep.get_client_by_id(client_id)
                if client:
                    client._last_name = input(f"Новая фамилия ({client._last_name}): ") or client._last_name
                    client._first_name = input(f"Новое имя ({client._first_name}): ") or client._first_name
                    client._middle_name = input(f"Новое отчество ({client._middle_name}): ") or client._middle_name
                    client._address = input(f"Новый адресс ({client._address}): ") or client._address
                    client._phone = input(f"Новый телефон ({client._phone}): ") or client._phone
                    client_rep.save_to_yaml()
                    print("Данные клиента изменены")
                else:
                    print("Клиент не найден")

            elif choice == "5":
                client_id = int(input("Введите ID клиента: "))
                client = client_rep.get_client_by_id(client_id)
                if client:
                    print("\nНайденный клиент:", client)
                else:
                    print("Клиент не найден.")

            elif choice == "6":
                k = int(input("Введите номер страницы (k): "))
                n = int(input("Введите количество клиентов на странице (n): "))
                short_list = client_rep.get_k_n_short_list(k, n)
                print(f"\nКраткая информация о клиентах на странице '{k}':", short_list)

            elif choice == "7":
                field = input("Введите поле для сортировки (client_id, last_name, first_name, middle_name, address, phone): ")
                client_rep.sort_by_field(field)
                print("\nОтсортированный список:", client_rep.clients)

            elif choice == "8":
                print("Выход")
                break
            else:
                print("Неверный выбор")
        except ValueError:
            print("Ошибка ввода данных. Пожалуйста, введите корректные значения")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
"""

if __name__ == "__main__":
    main()
