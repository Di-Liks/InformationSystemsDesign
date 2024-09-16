import yaml

class MyEntity_rep_yaml:
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file
        self.data = self.read_all()  # Чтение данных из файла при инициализации

    # a. Чтение всех значений из файла
    def read_all(self):
        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or []
        except FileNotFoundError:
            return []

    # b. Запись всех значений в файл
    def write_all(self):
        with open(self.yaml_file, 'w', encoding='utf-8') as file:
            yaml.dump(self.data, file, allow_unicode=True, default_flow_style=False)

    # c. Получить объект по ID
    def get_by_id(self, client_id):
        for client in self.data:
            if client['ClientID'] == client_id:
                return client
        return None

    # d. Получить список k по счету n объектов класса short
    def get_k_n_short_list(self, k, n):
        start_index = (n - 1) * k
        end_index = start_index + k
        return self.data[start_index:end_index]

    # e. Сортировать элементы по выбранному полю (например, по фамилии)
    def sort_by_field(self, field_name='LastName'):
        self.data.sort(key=lambda x: x.get(field_name, ''))
        self.write_all()

    # f. Добавить объект в список (при добавлении сформировать новый ID)
    def add_client(self, last_name, first_name, middle_name, address, phone):
        new_id = max([client['ClientID'] for client in self.data], default=0) + 1
        new_client = {
            'ClientID': new_id,
            'LastName': last_name,
            'FirstName': first_name,
            'MiddleName': middle_name,
            'Address': address,
            'Phone': phone
        }
        self.data.append(new_client)
        self.write_all()

    # g. Заменить элемент списка по ID
    def update_client_by_id(self, client_id, last_name=None, first_name=None, middle_name=None, address=None, phone=None):
        client = self.get_by_id(client_id)
        if client:
            if last_name:
                client['LastName'] = last_name
            if first_name:
                client['FirstName'] = first_name
            if middle_name:
                client['MiddleName'] = middle_name
            if address:
                client['Address'] = address
            if phone:
                client['Phone'] = phone
            self.write_all()
            return True
        return False

    # h. Удалить элемент списка по ID
    def delete_client_by_id(self, client_id):
        client = self.get_by_id(client_id)
        if client:
            self.data.remove(client)
            self.write_all()
            return True
        return False

    # i. Получить количество элементов
    def get_count(self):
        return len(self.data)
