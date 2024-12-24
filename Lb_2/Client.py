from dataclasses import field

from random import choice

import yaml
import json
import os

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


class ClientShort(Client):
    def __str__(self):
        return f"ClientShort(ID={self._client_id}, Фамилия={self._last_name}, Телефон={self._phone})"

class Client_rep_yaml:
    def __init__(self, filepath="clients.yaml"):
        self.filepath = filepath
        self.clients = []
        self.next_id = 1
        if os.path.exists(self.filepath):
            self.load_from_yaml()

    def load_from_yaml(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data:
                    for client_data in data:
                        self.clients.append(Client(*client_data.values()))
                    self.next_id = max(c._client_id for c in self.clients) + 1 if self.clients else 1
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Ошибка при загрузке из YAML: {e}")

    def save_to_yaml(self):
        try:
            data = [vars(c) for c in self.clients]
            with open(self.filepath, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Ошибка при сохранении в YAML: {e}")

    def get_client_by_id(self, client_id):
        for client in self.clients:
            if client._client_id == client_id:
                return client
        return None

    def get_k_n_short_list(self, k, n):
        return [ClientShort(c) for c in self.clients[(k-1)*n:(k-1)*n+n]]

    def sort_by_field(self, field):
        try:
            self.clients.sort(key=lambda x: getattr(x, f"_{field}"))
        except AttributeError:
            print(f"Поле '{field}' не найдено.")

    def add_client(self, last_name, first_name, middle_name, address, phone):
        new_client = Client(self.next_id, last_name, first_name, middle_name, address, phone)
        self.clients.append(new_client)
        self.next_id += 1
        self.save_to_yaml()
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
        self.save_to_yaml()

    def get_count(self):
        return len(self.clients)


class Client_rep_json:
    def __init__(self, filepath="clients.json"):
        self.filepath = filepath
        self.clients = []
        self.next_id = 1
        if os.path.exists(self.filepath):
            self.load_from_json()

    def load_from_json(self):
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                for item in data:
                    self.clients.append(Client(*item.values()))
                self.next_id = max(c._client_id for c in self.clients) + 1 if self.clients else 1
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке из JSON: {e}")

    def save_to_json(self):
        try:
            data = [vars(c) for c in self.clients]
            with open(self.filepath, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при сохранении в JSON: {e}")

    def get_client_by_id(self, client_id):
        for client in self.clients:
            if client._client_id == client_id:
                return client
        return None

    def get_k_n_short_list(self, k, n):
        return [ClientShort(c) for c in self.clients[(k-1)*n:(k-1)*n+n]]

    def sort_by_field(self, field):
        try:
            self.clients.sort(key=lambda x: getattr(x, f"_{field}"), reverse=False)
        except AttributeError:
            print(f"Поле '{field}' не найдено.")

    def add_client(self, last_name, first_name, middle_name, address, phone):
        new_client = Client(self.next_id, last_name, first_name, middle_name, address, phone)
        self.clients.append(new_client)
        self.next_id += 1
        self.save_to_json()
        return new_client

    def update_client(self, client_id, last_name, first_name, middle_name, address, phone):
        client = self.get_client_by_id(client_id)
        if client:
            client._last_name = last_name
            client._first_name = first_name
            client._middle_name = middle_name
            client._address = address
            client._phone = phone
            self.save_to_json()
            return True
        return False

    def delete_client(self, client_id):
        self.clients = [c for c in self.clients if c._client_id != client_id]
        self.save_to_json()

    def get_count(self):
        return len(self.clients)


def main():
    client_rep = Client_rep_yaml()
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
                field = input("Введите поле для сортировки (ClientID, last_name, first_name, middle_name, address, phone): ")
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

if __name__ == "__main__":
    main()
