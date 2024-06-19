# How to run this project
We will use the venv provided to run this project, the venv is located in the root of the project, to activate it you must run the following command:
```bash
python -m venv venv
source venv/bin/activate
```

Download some librabry.
```powershell
pip install django
pip install allauth
pip install explorer
```

```powershell
cd StoreMemory
python manage.py makemigrations user
python manage.py migrate
python manage.py runserver
```
