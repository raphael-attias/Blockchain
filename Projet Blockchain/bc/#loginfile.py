import json

a = str(input("ton prenom ? "))


class User:
    def __init__(self, username):
        self.username = username

    def to_dict(self):
        return {'username': self.username}

    def __str__(self):
        return f'Username: {self.username}'


class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_user(self, user):
        users = self._read_users()
        users.append(user.to_dict())
        self._write_users(users)

    def read_users(self):
        users = self._read_users()
        for user_data in users:
            user = User(user_data['username'])
            print(user)

    def update_user(self, username, new_email):
        users = self._read_users()
        for user_data in users:
            if user_data['username'] == username:
                user_data['email'] = new_email
                break
        self._write_users(users)

    def delete_user(self, username):
        users = self._read_users()
        users = [user_data for user_data in users if user_data['username'] != username]
        self._write_users(users)

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
new_user = User(a)
user_manager.create_user(new_user)

# Lecture des utilisateurs
print("Liste des utilisateurs :")
user_manager.read_users()

# Mise à jour de l'email d'un utilisateur
user_manager.update_user(a)

# Suppression d'un utilisateur
#user_manager.delete_user('john_doe')

# Lecture des utilisateurs après suppression
print("Liste des utilisateurs après suppression :")
user_manager.read_users()

#if a != user_manager:
    #user_manager.create_user
