class MyEntityRepYaml:
    def __init__(self, file_name):
        self.file_name = file_name
        self.clients = self._read_file()

    def _read_file(self):
        """Чтение данных из файла и преобразование их в объекты."""
        try:
            with open(self.file_name, 'r') as file:
                data = file.readlines()
                if data:
                    return self._parse_yaml(data)
                return []
        except FileNotFoundError:
            return []

    def _write_file(self):
        """Запись текущего состояния клиентов в файл."""
        with open(self.file_name, 'w') as file:
            file.write(self._convert_to_yaml(self.clients))

    def _parse_yaml(self, lines):
        """Парсинг данных в формате YAML."""
        objects = []
        obj = {}
        for line in lines:
            if line.strip() == '':
                if obj:
                    objects.append(obj)
                    obj = {}
                continue
            key, value = line.split(':', 1)
            obj[key.strip()] = value.strip()
        if obj:
            objects.append(obj)
        return objects

    def _convert_to_yaml(self, objects):
        """Конвертация объектов в строку формата YAML."""
        yaml_str = ""
        for obj in objects:
            for key, value in obj.items():
                yaml_str += f"{key}: {value}\n"
            yaml_str += "\n"
        return yaml_str

    def get_object_by_id(self, client_id):
        """Получить объект по ID."""
        for client in self.clients:
            if client['ClientID'] == str(client_id):
                return client
        return None

    def add_object(self, last_name, first_name, middle_name, address, phone):
        """Добавить новый объект с автоматическим присвоением ID."""
        new_id = str(max([int(client['ClientID']) for client in self.clients]) + 1 if self.clients else 1)
        new_client = {
            "ClientID": new_id,
            "LastName": last_name,
            "FirstName": first_name,
            "MiddleName": middle_name,
            "Address": address,
            "Phone": phone
        }
        self.clients.append(new_client)
        self._write_file()

    def update_object(self, client_id, last_name, first_name, middle_name, address, phone):
        """Обновить существующий объект по ID."""
        for client in self.clients:
            if client['ClientID'] == str(client_id):
                client['LastName'] = last_name
                client['FirstName'] = first_name
                client['MiddleName'] = middle_name
                client['Address'] = address
                client['Phone'] = phone
                self._write_file()
                return True
        return False

    def delete_object(self, client_id):
        """Удалить объект по ID."""
        self.clients = [client for client in self.clients if client['ClientID'] != str(client_id)]
        self._write_file()

    def get_k_n_short_list(self, k, n):
        """Получить k объектов начиная с n."""
        return self.clients[n:n+k]

    def sort_by_field(self, field_name):
        """Сортировать объекты по указанному полю."""
        self.clients.sort(key=lambda x: x[field_name])
        self._write_file()

    def get_count(self):
        """Получить количество объектов."""
        return len(self.clients)
