import json

class ClientBase:
    def __init__(self, last_name=None, first_name=None, middle_name=None, address=None, phone=None, data=None):
        if data:
            # Если передан data, проверим его тип (например, строка или JSON)
            if isinstance(data, str):
                # Попробуем распарсить как JSON
                try:
                    parsed_data = json.loads(data)
                    self.__init_from_dict(parsed_data)
                except json.JSONDecodeError:
                    # Если это не JSON, предположим, что это строка формата "Фамилия Имя Отчество Адрес Телефон"
                    self.__init_from_string(data)
            elif isinstance(data, dict):
                # Если это словарь, инициализируем из словаря
                self.__init_from_dict(data)
            else:
                raise ValueError("Invalid data format. Expected JSON string, plain string, or dictionary.")
        else:
            # Стандартный конструктор с отдельными аргументами
            self.__last_name = self.validate_field(last_name, "Last name", is_alpha=True, max_length=50)
            self.__first_name = self.validate_field(first_name, "First name", is_alpha=True, max_length=50)
            self.__middle_name = self.validate_field(middle_name, "Middle name", is_alpha=True, max_length=50)
            self.__address = self.validate_field(address, "Address", max_length=100)
            self.__phone = self.validate_field(phone, "Phone number", is_phone=True, exact_length=12)

    # Дополнительные конструкторы (вспомогательные методы)
    def __init_from_string(self, data_str):
        parts = data_str.split()
        if len(parts) != 5:
            raise ValueError("Invalid string format. Expected: 'LastName FirstName MiddleName Address Phone'")
        
        self.__last_name = self.validate_field(parts[0], "Last name", is_alpha=True, max_length=50)
        self.__first_name = self.validate_field(parts[1], "First name", is_alpha=True, max_length=50)
        self.__middle_name = self.validate_field(parts[2], "Middle name", is_alpha=True, max_length=50)
        self.__address = self.validate_field(parts[3], "Address", max_length=100)
        self.__phone = self.validate_field(parts[4], "Phone number", is_phone=True, exact_length=12)

    def __init_from_dict(self, data_dict):
        try:
            self.__last_name = self.validate_field(data_dict['last_name'], "Last name", is_alpha=True, max_length=50)
            self.__first_name = self.validate_field(data_dict['first_name'], "First name", is_alpha=True, max_length=50)
            self.__middle_name = self.validate_field(data_dict['middle_name'], "Middle name", is_alpha=True, max_length=50)
            self.__address = self.validate_field(data_dict['address'], "Address", max_length=100)
            self.__phone = self.validate_field(data_dict['phone'], "Phone number", is_phone=True, exact_length=12)
        except KeyError as e:
            raise ValueError(f"Missing key in JSON or dict: {e}")

    # Универсальный метод для валидации полей
    @staticmethod
    def validate_field(value, field_name, is_alpha=False, is_phone=False, max_length=None, exact_length=None):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

        if max_length and len(value) > max_length:
            raise ValueError(f"{field_name} must not exceed {max_length} characters")

        if exact_length and len(value) != exact_length:
            raise ValueError(f"{field_name} must be exactly {exact_length} characters")

        if is_alpha and not value.isalpha():
            raise ValueError(f"{field_name} must contain only alphabetic characters")

        if is_phone and (not value.startswith('+') or not value[1:].isdigit()):
            raise ValueError(f"{field_name} must be in the format '+1234567890'")

        return value

    # Геттеры для получения полей
    def get_last_name(self):
        return self.__last_name

    def get_first_name(self):
        return self.__first_name

    def get_middle_name(self):
        return self.__middle_name

    def get_address(self):
        return self.__address

    def get_phone(self):
        return self.__phone

    # Сравнение объектов на равенство
    def __eq__(self, other):
        if isinstance(other, ClientBase):
            return (self.__last_name == other.__last_name and
                    self.__first_name == other.__first_name and
                    self.__middle_name == other.__middle_name and
                    self.__address == other.__address and
                    self.__phone == other.__phone)
        return False


class Client(ClientBase):
    def __str__(self):
        #Возвращает полную версию информации о клиенте
        return (f"Client: {self.get_last_name()} {self.get_first_name()} {self.get_middle_name()}\n"
                f"Address: {self.get_address()}\n"
                f"Phone: {self.get_phone()}")


class ClientShortInfo(ClientBase):
    def __str__(self):
        #Возвращает краткую версию информации о клиенте
        return f"Client: {self.get_last_name()} {self.get_first_name()} - Phone: {self.get_phone()}"


# Пример использования
try:
    # Создаем объект Client (полная версия)
    client1 = Client("Ivanov", "Ivan", "Ivanovich", "123 Main St", "+1234567890")
    
    # Создаем объект ClientShortInfo (краткая версия)
    client_short_info = ClientShortInfo("Ivanov", "Ivan", "Ivanovich", "123 Main St", "+1234567890")
    
    # Вывод полной версии клиента
    print("Полная версия клиента:")
    print(client1)  # Output: Полная информация о клиенте
    
    # Вывод краткой версии клиента
    print("\nКраткая версия клиента:")
    print(client_short_info)  # Output: Краткая информация о клиенте

except ValueError as e:
    print(e)
