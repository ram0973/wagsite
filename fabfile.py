"""
Fabric2 file. Fabric2 docs here:
https://docs.fabfile.org/
http://www.fabfile.org/
This fabfile deploys app in requested environment
"""
import io
import random
import string
from jinja2 import Environment, FileSystemLoader
from fabric import task
from invoke import Exit
from patchwork.transfers import rsync

ENV_DEV = 'dev'
ENV_STAGING = 'staging'
ENV_PROD = 'prod'
ENVS = [ENV_DEV, ENV_STAGING, ENV_PROD]

BASE_DIR = '/webapps'
APP_NAME = 'wagsite'
APP_DIR = '{}/{}'.format(BASE_DIR, APP_NAME)
FABRIC_DIR = '{}/fabric'.format(APP_DIR)

APP_DOMAIN = 'localhost'
DJANGO_WSGI_MODULE = 'core.wsgi'
DJANGO_SETTINGS_MODULE = 'core.settings'
DJANGO_SECRET_KEY_LENGTH = 50
DOTENV_FILE = '{}/core/.env'.format(APP_DIR)
REPO = 'https://github.com/ram0973/djblog'

SUPERUSER_EMAIL = 'admin@{}'.format(APP_DOMAIN)
SUPERUSER_PASSWORD = 'pass'

DB_NAME = APP_NAME
DB_USER = APP_NAME
DB_PASSWORD = APP_NAME
DB_URL = 'postgresql://{}:{}@localhost/{}'  # DB_USER, DB_PASSWORD, DB_NAME

SERVER_LOCALE = 'ru_RU.UTF-8'
SERVER_TIMEZONE = 'UTC'

USER_GUNICORN = APP_NAME
USER_NGINX = 'nginx'
DEV_GROUP = 'webapps'

VENV_NAME = 'venv'
VENV_DIR = '{}/{}'.format(APP_DIR, VENV_NAME)
VENV_PYTHON = '{}/bin/python3'.format(VENV_DIR)

GECKO_VERSION = '0.25.0'


def render_template(templates_dir, template_name, payload):
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(template_name)
    return template.render(payload)


def put_rendered_template(ctx, rendered_template, outfile):
    file_object = io.StringIO()
    file_object.write(rendered_template)
    ctx.put(file_object, outfile, preserve_mode=False)


def check_envs(env):
    if env not in ENVS:
        print('Valid environments are: {} . Exiting.'.format(ENVS))
        raise Exit


def gathering_facts(ctx):
    os = ctx.run('lsb_release -is', hide=True).stdout.rstrip().lower()
    release = ctx.run('lsb_release -cs', hide=True).stdout.rstrip().lower()
    return {'os': os, 'release': release}


def get_django_secret_key(length):
    allowed_chars = string.ascii_letters+string.digits
    return ''.join(random.choice(allowed_chars) for _ in range(length))


@task
def prepare_server(ctx):
    """ Command: $ fab -e -H host prepare-server """
    ctx.run('sudo apt-get update')
    ctx.run('sudo timedatectl set-timezone {}'.format(SERVER_TIMEZONE))
    ctx.run('sudo apt-get install language-pack-ru -y')
    ctx.run('sudo localectl set-locale LANG={}'.format(SERVER_LOCALE))
    ctx.run('source /etc/default/locale')
    ctx.run('sudo apt-get install make git python3-venv -y')
    ctx.run('sudo groupadd --system {}'.format(DEV_GROUP), warn=True)
    ctx.run('sudo install -d -o {} -g {} -m ug=rwX {}'
            .format(ctx.user, DEV_GROUP, APP_DIR))
    print(ctx.user)
    ctx.run('sudo setfacl -R -m u:{}:rwX {}'.format(ctx.user, APP_DIR))
    ctx.run('sudo setfacl -Rd -m u:{}:rwX {}'.format(ctx.user, APP_DIR))


@task
def rsync_src(ctx):
    """ Command: $ fab -e -H host rsync-src """
    rsync(ctx, source='.', target=APP_DIR,
          exclude=(VENV_NAME, '.idea', '.vagrant'),
          delete=True, strict_host_keys=True, rsync_opts='-rz', ssh_opts='')


@task
def clone_git_src(ctx, repo):
    """ Command: $ fab -e -H host clone-git-src --repo=REPO """
    is_git_folder_exists = ctx.run('test -d {}/.git'.format(APP_DIR), warn=True)
    if is_git_folder_exists:
        ctx.run('cd {} && git reset --hard HEAD'.format(APP_DIR))
        ctx.run('cd {} && git pull origin master'.format(APP_DIR))
    else:
        ctx.run('cd {} && git clone {} {}'.format(BASE_DIR, repo, APP_DIR))


@task
def install_requirements(ctx, env):
    """ Command: $ fab -e -H host install-requirements --env=ENV """
    check_envs(env)
    # ctx.run('rm -rf {}'.format(VENV_DIR))
    ctx.run('cd {} && python3 -m venv {}'.format(APP_DIR, VENV_DIR))
    ctx.run('cd {} && source {}/bin/activate && pip install wheel'
            ' && pip install -r requirements/{}.txt'
            .format(APP_DIR, VENV_DIR, env))


@task
def configure_env_file(ctx, env, db_url, domain, sentry_dsn):
    """ Command: $ fab -e -H host configure-env-file --env=ENV --db_url=DB_URL \
--domain=DOMAIN --sentry_dsn=SENTRY_DSN """
    check_envs(env)
    env_file_exists = ctx.run('test -e {}'.format(DOTENV_FILE), warn=True)
    if env_file_exists:
        ctx.run('mv -f {} {}.bak'.format(DOTENV_FILE, DOTENV_FILE))
    django_secret_key = get_django_secret_key(DJANGO_SECRET_KEY_LENGTH)
    payload = {'django_secret_key': django_secret_key,
               'django_settings_module': DJANGO_SETTINGS_MODULE,
               'env': env, 'db_url': db_url, 'app_domain': domain,
               'sentry_dsn': sentry_dsn}
    dotenv_file = render_template(FABRIC_DIR, 'env.j2', payload)
    put_rendered_template(ctx, dotenv_file, DOTENV_FILE)
    ctx.run('source {}'.format(DOTENV_FILE))


@task
def configure_gunicorn(ctx, env):
    """ Command: $ fab -e -H host configure-gunicorn --env=ENV """
    check_envs(env)
    ctx.run('sudo useradd --system --home {} {}'.format(APP_DIR, USER_GUNICORN),
            warn=True)
    ctx.run('sudo setfacl -R -m u:{}:rX {}'.format(USER_GUNICORN, APP_DIR))
    ctx.run('sudo setfacl -Rd -m u:{}:rX {}'.format(USER_GUNICORN, APP_DIR))
    ctx.run('sudo setfacl -R -m u:{}:rwX {}/run'.format(USER_GUNICORN, APP_DIR))
    ctx.run('sudo setfacl -Rd -m u:{}:rwX {}/run'
            .format(USER_GUNICORN, APP_DIR))
    ctx.run('sudo setfacl -R -m u:{}:rwX {}/public/{{media,uploads}}'
            .format(USER_GUNICORN, APP_DIR))
    ctx.run('sudo setfacl -Rd -m u:{}:rwX {}/public/{{media,uploads}}'
            .format(USER_GUNICORN, APP_DIR))
    payload = {'app_dir': APP_DIR, 'app_name': APP_NAME,
               'env': env.capitalize(),
               'django_settings_module': DJANGO_SETTINGS_MODULE,
               'user_gunicorn': USER_GUNICORN}
    gunicorn_conf = render_template(FABRIC_DIR, 'gunicorn.service.j2', payload)
    put_rendered_template(ctx, gunicorn_conf, '{}/{}.service'
                          .format(FABRIC_DIR, APP_NAME))
    ctx.run('sudo mv -f {}/{}.service /etc/systemd/system/{}.service'
            .format(FABRIC_DIR, APP_NAME, APP_NAME))
    ctx.run('sudo systemctl daemon-reload')
    ctx.run('sudo systemctl enable {}'.format(APP_NAME))
    ctx.run('sudo systemctl restart {}'.format(APP_NAME))


@task
def install_psql(ctx):
    """ Command: $ fab -e -H host install-psql"""
    ctx.run('sudo apt-get install postgresql -y')
    ctx.run('sudo systemctl enable postgresql')
    ctx.run('sudo systemctl restart postgresql')


@task
def configure_psql(ctx, db_user, db_password, db_name):
    """ Command: $ fab -e -H host configure-psql db_user=DB_USER \
db_password=DB_PASSWORD db_name=DB_NAME """
    ctx.run('sudo sed -i \"s/#listen_address.*/listen_addresses'
            ' \'localhost\'/\" /etc/postgresql/10/main/postgresql.conf')
    ctx.run('sudo -u postgres createdb {} -E UTF-8'
            .format(db_name), warn=True)
    ctx.run('sudo -u postgres createuser {}'
            .format(db_user), warn=True)
    ctx.run('sudo -u postgres psql -c '
            '"ALTER USER {} WITH ENCRYPTED PASSWORD \'{}\'"'
            .format(db_user, db_password))
    ctx.run('sudo -u postgres psql -c '
            '"ALTER USER {} WITH NOSUPERUSER NOCREATEROLE LOGIN CREATEDB"'
            .format(db_user)) # CREATEDB - for tests, LOGIN - for migrations
    ctx.run('sudo -u postgres psql -c "GRANT USAGE ON SCHEMA public TO {};"'
            .format(db_user))
    ctx.run('sudo -u postgres psql -c '
            '"GRANT ALL PRIVILEGES ON DATABASE {} TO {};"'
            .format(db_name, db_user))
    ctx.run('sudo -u postgres psql {} -c "GRANT ALL ON ALL TABLES IN SCHEMA '
            'public TO {};"'.format(db_name, db_user))
    ctx.run('sudo -u postgres psql {} -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA '
            'public TO {};"'.format(db_name, db_user))
    ctx.run('sudo -u postgres psql {} -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA '
            'public TO {};"'.format(db_name, db_user))
    ctx.run('sudo -u postgres psql -c "ALTER DEFAULT PRIVILEGES IN SCHEMA '
            'public GRANT ALL ON TABLES TO {};"'.format(db_user))
    ctx.run('sudo systemctl restart postgresql')


@task
def install_nginx_mainline(ctx):
    """ Command: $ fab -e -H host install-nginx-mainline """
    ctx.run('sudo apt-get remove nginx -y')
    facts = gathering_facts(ctx)
    ctx.run('curl -fsSL https://nginx.org/keys/nginx_signing.key |'
            ' sudo apt-key add -')
    ctx.run('sudo add-apt-repository "deb http://nginx.org/packages/mainline/{}'
            ' {} nginx"'
            .format(facts['os'], facts['release']))
    ctx.run('sudo apt-get install nginx -y')
    ctx.run('sudo rm -f /etc/nginx/conf.d/default.conf', warn=True)
    ctx.run('sudo systemctl enable nginx')
    ctx.run('sudo systemctl restart nginx')


@task
def configure_nginx(ctx, env, domain):
    """ Command: $ fab -e -H host configure-nginx --env=ENV --domain=DOMAIN """
    check_envs(env)
    ctx.run('sudo adduser --system --no-create-home --shell /bin/false '
            '--group --disabled-login {}'.format(USER_NGINX))
    ctx.run('sudo setfacl -R -m u:{}:rX {}'.format(USER_NGINX, APP_DIR))
    ctx.run('sudo setfacl -Rd -m u:{}:rX {}'.format(USER_NGINX, APP_DIR))
    ctx.run('sudo setfacl -R -m u:{}:rwX {}/public/{{media,uploads}}'
            .format(USER_NGINX, APP_DIR))
    ctx.run('sudo setfacl -Rd -m u:{}:rwX {}/public/{{media,uploads}}'
            .format(USER_NGINX, APP_DIR))
    ctx.run('sudo setfacl -R -m u:{}:rwX {}/run'.format(USER_NGINX, APP_DIR))
    ctx.run('sudo setfacl -Rd -m u:{}:rwX {}/run'.format(USER_NGINX, APP_DIR))
    ctx.run('sudo rm -f /etc/nginx/conf.d/default.conf', warn=True)
    if env == ENV_DEV or env == ENV_STAGING:
        ctx.run('sudo mkdir -p /etc/letsencrypt/live/{}'.format(domain))
        ctx.run('sudo cp {}/local_certs/* /etc/letsencrypt/live/{}'
                .format(FABRIC_DIR, domain))
        ctx.run('sudo cp {}/local_certs/ssl-dhparams.pem /etc/letsencrypt'
                .format(FABRIC_DIR))
    elif env == ENV_PROD:
        ctx.run('sudo add-apt-repository -y ppa:certbot/certbot')
        ctx.run('sudo apt-get install certbot -y')
    payload = {'app_domain': domain, 'app_dir': APP_DIR, 'app_name': APP_NAME,
               'env': env}
    nginx_conf = render_template(FABRIC_DIR, 'nginx.conf.j2', payload)
    put_rendered_template(ctx, nginx_conf, '{}/{}.{}.conf'
                          .format(FABRIC_DIR, domain, APP_NAME))
    ctx.run('sudo mv -f {}/{}.{}.conf /etc/nginx/conf.d/{}.{}.conf'
            .format(FABRIC_DIR, domain, APP_NAME, domain, APP_NAME))
    ctx.run('sudo systemctl restart nginx')


@task
def collect_static(ctx):
    """ Command: $ fab -e -H host collect-static """
    ctx.run('cd {} && source {}/bin/activate && {} manage.py '
            'collectstatic --noinput'.format(APP_DIR, VENV_DIR, VENV_PYTHON),
            pty=True)


@task
def migrate(ctx):
    """ Command: $ fab -e -H host migrate """
    ctx.run('cd {} && source {}/bin/activate && '
            '{} manage.py makemigrations --noinput && '
            '{} manage.py migrate --noinput'
            .format(APP_DIR, VENV_DIR, VENV_PYTHON, VENV_PYTHON), pty=True)


@task
def create_django_su(ctx, email, password):
    """ Command: $ fab -e -H host create-django-su --email=EMAIL \
--password=PASSWORD """
    ctx.run('cd {} && source {}/bin/activate && export PYTHONIOENCODING="UTF-8"'
            ' && {} manage.py createcustomsuperuser --email {} --password {}'
            .format(APP_DIR, VENV_DIR, VENV_PYTHON, email, password), pty=True)


@task
def gecko(ctx):
    """ Command: $ fab -e -H host gecko """
    ctx.run('sudo apt-get install -y ca-certificates curl firefox')
    ctx.run('curl -L https://github.com/mozilla/geckodriver/releases/download/v{}/'
            'geckodriver-v{}-linux64.tar.gz | sudo tar xz -C /usr/local/bin'
            .format(GECKO_VERSION, GECKO_VERSION))


def deploy(ctx, env, repo, db_user, db_password, db_name, domain, su_email,
           su_password, sentry_dsn):
    print('Task started')
    db_url = DB_URL.format(db_user, db_password, db_name)
    check_envs(env)
    prepare_server(ctx)
    if env == ENV_DEV:
        rsync_src(ctx)
    elif env == ENV_STAGING or env == ENV_PROD:
        clone_git_src(ctx, repo)
    install_requirements(ctx, env)
    configure_env_file(ctx, env, db_url, domain, sentry_dsn)
    if env == ENV_STAGING or env == ENV_PROD:
        configure_gunicorn(ctx, env)
    install_psql(ctx)
    configure_psql(ctx, db_user, db_password, db_name)
    install_nginx_mainline(ctx)
    configure_nginx(ctx, env, domain)
    collect_static(ctx)
    migrate(ctx)
    create_django_su(ctx, su_email, su_password)
    if env == ENV_DEV or env == ENV_STAGING:
        gecko(ctx)
    print('Task finished')

@task
def deploy_local(ctx, env, repo=REPO, db_user=DB_USER, db_password=DB_PASSWORD,
                 db_name=DB_NAME, domain=APP_DOMAIN, su_email=SUPERUSER_EMAIL,
                 su_password=SUPERUSER_PASSWORD, sentry_dsn=''):
    """ Command: $ fab -e -H host deploy-local --env=ENV{dev,staging} """
    deploy(ctx, env, repo, db_user, db_password, db_name, domain, su_email,
           su_password, sentry_dsn)


def input_default(name, default_value):
    user_input = input('Enter {}:[{}] '.format(name, default_value))
    return default_value if not user_input else user_input


@task
def deploy_prod(ctx):
    """ Command: $ fab -e -H host deploy-prod """
    domain = input_default('domain', APP_DOMAIN)
    db_name = input_default('db name', DB_USER)
    db_user = input_default('db user', DB_USER)
    db_password = input_default('db password', DB_PASSWORD)
    sentry_dsn = input('Sentry DSN: ')
    su_email = input_default('superuser email', 'admin@{}'.format(domain))
    su_password = input_default('superuser password', SUPERUSER_PASSWORD)
    deploy(ctx, ENV_PROD, REPO, db_user, db_password, db_name, domain, su_email,
           su_password, sentry_dsn)


@task
def status(ctx):
    """ Command: $ fab -e -H host status """
    ctx.run('sudo systemctl status nginx', warn=True)
    ctx.run('sudo journalctl -e -u nginx', warn=True)
    ctx.run('sudo netstat -tulpn | grep nginx', warn=True)
    ctx.run('sudo systemctl status postgresql', warn=True)
    ctx.run('sudo journalctl -e -u postgresql', warn=True)
    ctx.run('sudo systemctl status {}'.format(APP_NAME), warn=True)
    ctx.run('sudo journalctl -e -u {}'.format(APP_NAME), warn=True)
    ctx.run('sudo systemctl --failed', warn=True)
