class Client:
    def __init__(self, LastName, FirstName, MiddleName, Address, Phone):
        self.LastName = LastName
        self.FirstName = FirstName
        self.MiddleName = MiddleName
        self.Address = Address
        self.Phone = Phone

    def to_dict(self):
        return {
            'LastName': self.LastName,
            'FirstName': self.FirstName,
            'MiddleName': self.MiddleName,
            'Address': self.Address,
            'Phone': self.Phone
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            LastName=data['LastName'],
            FirstName=data['FirstName'],
            MiddleName=data['MiddleName'],
            Address=data['Address'],
            Phone=data['Phone']
        )