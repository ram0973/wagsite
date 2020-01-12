## PROJECT HISTORY

**Start project**

```bash
$ pip install django
$ django-admin startproject ssn
$ cd ssn
$ python manage.py runserver
```
Opened http://127.0.0.1/ - Django is running ok.

**Django-configurations integration**:
```bash
pip install django-configurations
pip install dj-database-url
```

Changed settings.py as here:
https://github.com/jazzband/django-configurations/blob/templates/1.8.x/project_name/settings.py

DB Paths remainder:
PostgreSQL postgres://USER:PASSWORD@HOST:PORT/NAME
SQLite sqlite:///PATH

Added ALLOWED_HOSTS in Prod config (to test Prod config):
```python

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', ]
```
Then
```bash
export DJANGO_CONFIGURATION=Dev
export DJANGO_SETTINGS_MODULE=ssn.settings
```

**Database creation, migration, seed**

Near manage.py created .env with DJANGO_SECRET_KEY variable, then:
```bash
python manage.py migrate
python manage.py createsuperuser
```

**Static files setup**:

Added public directory with 'static' and 'media' folders inside, then
in urls.py:
```python
if os.getenv('DJANGO_CONFIGURATION') == 'Dev':
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
```
In settings.py:
```python
PUBLIC_DIR = BASE_DIR / 'public'
STATIC_ROOT = PUBLIC_DIR / 'static'
MEDIA_ROOT = PUBLIC_DIR / 'media'
```
Then ran the collectstatic management command:
```bash
$ python manage.py collectstatic
$ pip freeze >requirements.txt
```
**Sentry integration**
```bash
pip install raven --upgrade
```
Copied client key from: Sentry project - Data - Client Keys to .env file as
SENTRY_DSN=project_secret_sentry_dsn (DSN means Data Source Name)
then in settings.py:
```python
INSTALLED_APPS = (
    'raven.contrib.django.raven_compat',
)
...
RAVEN_CONFIG = {
    'dsn': values.Value(environ_name='SENTRY_DSN'),
    # Release based on the git info.
    'release': raven.fetch_git_sha(str(BASE_DIR)),
}
```
Then added raven middleware and logging to sentry.
https://docs.sentry.io/clients/python/integrations/django/

Then Sentry config tested:
```bash
python manage.py raven test
```
In the project on Sentry.io got a message:
This is a test message generated using ``raven test``

**Local tests coverage and CI**

Added local tests coverage support with settings in .coveragerc:
```bash
$ pip install coverage
# If you want to show the results in the command line, run:
$ coverage report
# For more readable reports:
$ coverage html
```
Added Continuous Integration with https://circleci.com:
1) Created repository (imported from GitHub)
2) Created .circleci/config.yml
3) On every git commit the application run tests on https://circleci.com

**Auth app and user info page**
```bash
python manage.py startapp auth
```