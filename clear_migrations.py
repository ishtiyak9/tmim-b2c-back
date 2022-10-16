import os
import shutil
import django
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tmmim.settings")
django.setup()

db_name = connection.settings_dict['NAME']
listdir = os.listdir()

for elem in listdir:
    if os.path.isdir(elem) and ('migrations' in os.listdir(elem)):
        migrations = os.listdir(f"{elem}/migrations")
        for migration in migrations:
            if migration != '__init__.py':
                # removing __pycache__ inside migrations
                if migration == "__pycache__":
                    shutil.rmtree(f"{elem}/migrations/{migration}")   
                # normal migration files
                else:
                    os.remove(f"{elem}/migrations/{migration}")
print("migration files are cleared successfully!")

for elem in listdir:
    if os.path.isdir(elem) and ('__pycache__' in os.listdir(elem)):
        shutil.rmtree(f"{elem}/__pycache__/")
print("__pycache__ files are cleared successfully!")

cursor = connection.cursor()
sql = f"DROP DATABASE {db_name}; CREATE DATABASE {db_name};"
cursor.execute(sql)
print("DB is cleared successfully!")
