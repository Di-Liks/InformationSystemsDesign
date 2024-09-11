class Client:
    def __init__(self, last_name, first_name, middle_name, address, phone):
        if not self.validate_last_name(last_name):
            raise ValueError("Invalid last name")
        if not self.validate_first_name(first_name):
            raise ValueError("Invalid first name")
        if not self.validate_middle_name(middle_name):
            raise ValueError("Invalid middle name")
        if not self.validate_address(address):
            raise ValueError("Invalid address")
        if not self.validate_phone(phone):
            raise ValueError("Invalid phone number")
        
        self.__last_name = last_name
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__address = address
        self.__phone = phone

    # Геттеры
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

    # Сеттеры с валидацией
    def set_last_name(self, last_name):
        if self.validate_last_name(last_name):
            self.__last_name = last_name
        else:
            raise ValueError("Invalid last name")

    def set_first_name(self, first_name):
        if self.validate_first_name(first_name):
            self.__first_name = first_name
        else:
            raise ValueError("Invalid first name")

    def set_middle_name(self, middle_name):
        if self.validate_middle_name(middle_name):
            self.__middle_name = middle_name
        else:
            raise ValueError("Invalid middle name")

    def set_address(self, address):
        if self.validate_address(address):
            self.__address = address
        else:
            raise ValueError("Invalid address")

    def set_phone(self, phone):
        if self.validate_phone(phone):
            self.__phone = phone
        else:
            raise ValueError("Invalid phone number")

    # Статические методы для валидации полей
    @staticmethod
    def validate_last_name(last_name):
        return isinstance(last_name, str) and last_name.isalpha() and 1 <= len(last_name) <= 50

    @staticmethod
    def validate_first_name(first_name):
        return isinstance(first_name, str) and first_name.isalpha() and 1 <= len(first_name) <= 50

    @staticmethod
    def validate_middle_name(middle_name):
        return isinstance(middle_name, str) and middle_name.isalpha() and 1 <= len(middle_name) <= 50

    @staticmethod
    def validate_address(address):
        return isinstance(address, str) and len(address) > 0 and len(address) <= 100

    @staticmethod
    def validate_phone(phone):
        # Допустим, что номер телефона должен быть строкой в формате "+1234567890"
        return isinstance(phone, str) and phone.startswith('+') and phone[1:].isdigit() and len(phone) == 12

    # Метод для отображения информации о клиенте
    def display_info(self):
        return (f"Client: {self.__last_name} {self.__first_name} {self.__middle_name}\n"
                f"Address: {self.__address}\n"
                f"Phone: {self.__phone}")

# Пример использования:
try:
    client = Client("Ivanov", "Ivan", "Ivanovich", "123 Main St", "+1234567890")
    print(client.display_info())

    # Попробуем установить некорректный номер телефона
    client.set_phone("12345")  # Это вызовет ошибку
except ValueError as e:
    print(e)
