class FileEntityRep:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self._read_file()

    def _read_file(self):
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
                clients = []
                for line in lines[1:]:
                    client_data = line.strip().split(',')
                    clients.append({
                        "ClientID": client_data[0],
                        "LastName": client_data[1],
                        "FirstName": client_data[2],
                        "Age": int(client_data[3])
                    })
                return clients
        except FileNotFoundError:
            return []

    def _write_file(self):
        with open(self.file_name, 'w') as file:
            file.write("ClientID,LastName,FirstName,Age\n")
            for client in self.data:
                file.write(f"{client['ClientID']},{client['LastName']},{client['FirstName']},{client['Age']}\n")

    def get_k_n_short_list(self, k, n):
        return self.data[n:n+k]

    def get_count(self):
        return len(self.data)

class FilterSortDecorator:
    def __init__(self, file_entity_rep, filter_function=None, sort_key=None):
        """
        :param file_entity_rep: объект класса FileEntityRep (или его наследника)
        :param filter_function: функция фильтрации объектов
        :param sort_key: ключ для сортировки объектов
        """
        self.file_entity_rep = file_entity_rep
        self.filter_function = filter_function
        self.sort_key = sort_key

    def get_k_n_short_list(self, k, n):
        """
        Получить отфильтрованный и отсортированный список из k объектов, начиная с n.
        :param k: количество объектов
        :param n: с какого объекта начинать
        :return: отфильтрованный и отсортированный список объектов
        """
        data = self.file_entity_rep.data

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
        data = self.file_entity_rep.data

        # Применение фильтрации
        if self.filter_function:
            data = list(filter(self.filter_function, data))

        return len(data)
