from .site_user import Site_userInSchema

# Пример использования для создания нового пользователя
user_data = {
    "username": "new_user",
    "password": "secure_password",
    "full_name": "John Doe"
}

# user_schema содержит валидированные данные, которые можно использовать для создания нового пользователя в базе данных
user_schema = Site_userInSchema(**user_data)

