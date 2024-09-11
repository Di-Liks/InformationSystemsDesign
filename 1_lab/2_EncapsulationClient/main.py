class Client:
    def __init__(self, last_name, first_name, middle_name, address, phone):
        self.__last_name = self.validate_field(last_name, "Last name", is_alpha=True, max_length=50)
        self.__first_name = self.validate_field(first_name, "First name", is_alpha=True, max_length=50)
        self.__middle_name = self.validate_field(middle_name, "Middle name", is_alpha=True, max_length=50)
        self.__address = self.validate_field(address, "Address", max_length=100)
        self.__phone = self.validate_field(phone, "Phone number", is_phone=True, exact_length=12)

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
        self.__last_name = self.validate_field(last_name, "Last name", is_alpha=True, max_length=50)

    def set_first_name(self, first_name):
        self.__first_name = self.validate_field(first_name, "First name", is_alpha=True, max_length=50)

    def set_middle_name(self, middle_name):
        self.__middle_name = self.validate_field(middle_name, "Middle name", is_alpha=True, max_length=50)

    def set_address(self, address):
        self.__address = self.validate_field(address, "Address", max_length=100)

    def set_phone(self, phone):
        self.__phone = self.validate_field(phone, "Phone number", is_phone=True, exact_length=12)

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

    # Метод для отображения информации о клиенте
    def display_info(self):
        return (f"Client: {self.__last_name} {self.__first_name} {self.__middle_name}\n"
                f"Address: {self.__address}\n"
                f"Phone: {self.__phone}")

# Пример использования
try:
    client = Client("Ivanov", "Ivan", "Ivanovich", "123 Main St", "+1234567890")
    print(client.display_info())

    # Обновление данных клиента
    client.set_phone("+0987654321")
    print(f"Updated phone: {client.get_phone()}")
    
except ValueError as e:
    print(e)
