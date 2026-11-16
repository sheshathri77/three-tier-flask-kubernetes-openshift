import os

master_username = os.getenv("DB_USER", "todo_user")
db_password = os.getenv("DB_PASSWORD", "todo_password")
endpoint = os.getenv("DB_HOST", "mysql:3306")
db_instance_name = os.getenv("DB_NAME", "tododb")