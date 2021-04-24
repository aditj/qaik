# qaik
Quantum AI Powered Microblogging

# How to run this on local machine?
- Clone this repo
- Create a virtual environment `virtualenv env`
- activate Virtual environment `source env/bin/activate`
- Install Requirements `pip install -r requirements.txt`
- Create empty folder at main with name `migrations` with an empty file `__init__.py` in it
- Make migrations and migrate to initialize db: `python3 manage.py makemigrations` and `python3 manage.py migrate`
- Run Server! `python3 manage.py runserver`
