# Базовый класс для работы с БД
class DBEntityRep:
    def __init__(self, db_data):
        """
        :param db_data: список данных, представляющих записи из БД
        """
        self.db_data = db_data

    def get_k_n_short_list(self, k, n):
        """
        Получить список из k объектов, начиная с n.
        :param k: количество объектов для возврата
        :param n: с какого объекта начинать
        :return: список объектов
        """
        return self.db_data[n:n+k]

    def get_count(self):
        """
        Получить количество объектов.
        :return: количество объектов
        """
        return len(self.db_data)


# Декоратор для фильтрации и сортировки
class FilterSortDecorator:
    def __init__(self, db_entity_rep, filter_function=None, sort_key=None):
        """
        :param db_entity_rep: объект класса DBEntityRep (или его наследника)
        :param filter_function: функция фильтрации объектов (если требуется)
        :param sort_key: ключ для сортировки объектов (если требуется)
        """
        self.db_entity_rep = db_entity_rep
        self.filter_function = filter_function
        self.sort_key = sort_key

    def get_k_n_short_list(self, k, n):
        """
        Получить отфильтрованный и отсортированный список из k объектов, начиная с n.
        :param k: количество объектов для возврата
        :param n: с какого объекта начинать
        :return: отфильтрованный и отсортированный список объектов
        """
        data = self.db_entity_rep.db_data

        # Применение фильтрации
        if self.filter_function:
            data = list(filter(self.filter_function, data))

        # Применение сортировки
        if self.sort_key:
            data.sort(key=self.sort_key)

        # Возврат отфильтрованного и отсортированного списка
        return data[n:n+k]

    def get_count(self):
        """
        Получить количество отфильтрованных объектов.
        :return: количество отфильтрованных объектов
        """
        data = self.db_entity_rep.db_data

        # Применение фильтрации
        if self.filter_function:
            data = list(filter(self.filter_function, data))

        return len(data)

# Пример данных
db_data = [
    {"ClientID": 1, "LastName": "Ivanov", "FirstName": "Ivan", "Age": 30},
    {"ClientID": 2, "LastName": "Petrov", "FirstName": "Petr", "Age": 25},
    {"ClientID": 3, "LastName": "Sidorov", "FirstName": "Sergey", "Age": 35},
    {"ClientID": 4, "LastName": "Nikolaev", "FirstName": "Nikolay", "Age": 28},
]

# Базовый объект класса для работы с БД
db_entity_rep = DBEntityRep(db_data)

# Пример фильтрации (возраст больше 28) и сортировки по возрасту
filter_function = lambda client: client["Age"] > 28
sort_key = lambda client: client["Age"]

# Применение декоратора для фильтрации и сортировки
decorated_rep = FilterSortDecorator(db_entity_rep, filter_function, sort_key)

# Получение отфильтрованного и отсортированного списка
print("Отфильтрованные и отсортированные записи (возраст > 28):")
print(decorated_rep.get_k_n_short_list(2, 0))  # Возвращает первых 2 клиента, возраст > 28

# Получение количества отфильтрованных записей
print("Количество отфильтрованных записей (возраст > 28):")
print(decorated_rep.get_count())
