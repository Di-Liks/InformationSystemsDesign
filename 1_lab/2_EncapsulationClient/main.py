class Client:
    def __init__(self, last_name, first_name, middle_name, address, phone):
        self.__last_name = last_name      # Приватное поле
        self.__first_name = first_name    # Приватное поле
        self.__middle_name = middle_name  # Приватное поле
        self.__address = address          # Приватное поле
        self.__phone = phone              # Приватное поле

    # Геттеры для полей
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

    # Сеттеры для полей
    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_middle_name(self, middle_name):
        self.__middle_name = middle_name

    def set_address(self, address):
        self.__address = address

    def set_phone(self, phone):
        self.__phone = phone

    # Метод для отображения информации о клиенте
    def display_info(self):
        return (f"Client: {self.__last_name} {self.__first_name} {self.__middle_name}\n"
                f"Address: {self.__address}\n"
                f"Phone: {self.__phone}")

# Пример использования:
client = Client("Ivanov", "Ivan", "Ivanovich", "123 Main St", "+1234567890")

# Доступ к полям через методы
print(client.display_info())

# Обновление данных клиента через сеттеры
client.set_phone("+0987654321")
print(f"Updated phone: {client.get_phone()}")
