import json

class User:
    def __init__(self, wallet, name, keypc, keype):
        self.wallet = wallet
        self.name = name
        self.keypc = keypc
        self.keype = keype

    def to_dict(self):
        return {'full_name': self.full_name, 'email': self.email}

    def __str__(self):
        return f'Full Name: {self.full_name}, Email: {self.email}'


class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_user(self):
        full_name = input("Enter your full name: ")
        email = input("Enter your email: ")
        user = User(full_name, email)

        users = self._read_users()
        users.append(user.to_dict())
        self._write_users(users)

    def read_users(self):
        users = self._read_users()
        for user_data in users:
            user = User(user_data['full_name'], user_data['email'])
            print(user)

    def _read_users(self):
        try:
            with open(self.file_path, 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []
        return users

    def _write_users(self, users):
        with open(self.file_path, 'w') as file:
            json.dump(users, file, indent=4)


# Exemple d'utilisation
user_manager = UserManager('users.json')

# Création d'un nouvel utilisateur
user_manager.create_user()

# Lecture des utilisateurs
print("Liste des utilisateurs :")
user_manager.read_users()
