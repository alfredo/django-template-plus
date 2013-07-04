import functools
import random
import os

from datetime import datetime
from fabric.api import local, env, lcd
from fabric.colors import yellow, red, green
from fabric.contrib import console

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
here = lambda *x: os.path.join(PROJECT_ROOT, *x)


def production():
    """Connection details for the ``production`` app"""
    env.slug = 'production'
    env.url = 'http://{{ heroku_app }}.herokuapp.com/'
    env.app = '{{ heroku_app }}'


def is_vm():
    """Determines if the script is running in a VM"""
    return os.environ['USER'] == 'vagrant'

IS_VM = is_vm()


def only_outside_vm(function):
    """Decorator to allow only ``inside`` VM commands """
    @functools.wraps(function)
    def inner(*args, **kwargs):
        if IS_VM:
            print red('Command can only be OUTSIDE the VM.')
            return exit(1)
        return function(*args, **kwargs)
    return inner


def only_inside_vm(function):
    """Decorator to allow only ``outside`` VM commands"""
    @functools.wraps(function)
    def inner(*args, **kwargs):
        if not IS_VM:
            print red('Command can only be INSIDE the VM.')
            return exit(1)
        return function(*args, **kwargs)
    return inner


def dj_heroku(command, slug, capture=False):
    """Runs a given django management command in the given Heroku's app."""
    new_cmd = ('heroku run django-admin.py %s --settings={{ project_name }}.'
               'settings.%s --remote %s' % (command, slug, slug))
    return local(new_cmd, capture)


def run_heroku(cmd, slug, capture=True):
    """Runs a Heroku command with the given ``remote``"""
    return local('heroku %s --app %s' % (cmd, slug), capture=capture)


@only_outside_vm
def collectstatic():
    print yellow('Compressing the static assets.')
    dj_heroku('compress --force', env.slug)
    print yellow('Uploading static assets to S3.')
    dj_heroku('collectstatic --noinput', env.slug)


@only_outside_vm
def syncdb():
    print yellow('Syncing %s database.' % env.slug)
    dj_heroku('syncdb --noinput', env.slug)


@only_outside_vm
def deploy(confirmation=''):
    """Deploys the given build."""
    confirmation = False if confirmation == 'False' else True
    SLUG = env.slug.upper()
    if env.slug not in ['production']:
        print red('Invaid destination: %s.' % SLUG)
        exit(3)
    if confirmation and env.slug == 'production':
        msg = red('You are about to DEPLOY %s to Heroku. Procceed?' % SLUG)
        if not console.confirm(msg):
            print yellow('Phew, aborted.')
            exit(2)
    print yellow('Deploying to %s. Because you said so.' % SLUG)
    with lcd(PROJECT_ROOT):
        print yellow('Pushing changes to %s in Heroku.' % SLUG)
        local('git push %s master --force' % env.slug)
        collectstatic()
        syncdb()
    print yellow('URL: %s' % env.url)
    print red('Done?')
    print '%s' % datetime.now()


def test():
    print red('We need tests!')


def _get_secret_key():
    return ("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^"
                                   "&*(-_=+)") for i in range(50)]))


@only_outside_vm
def setup_heroku():
    msg = """"Executing this command will add the following Heroku
environment variables ``DJANGO_SETTINGS_MODULE`` and  ``SECRET_KEY``.
As well provision a heroku-postgresql:dev server, if no one has been created.
"""
    print green(msg)
    if not console.confirm(yellow('Proceed?')):
        print yellow('Phew, aborted.')
        exit(1)
    response = local('heroku config', capture=True)
    response_list = response.splitlines()
    # Verify this is a valid heroku setup
    if not 'Config Vars' in response_list[0]:
        print red('No heroku installation detected.')
        exit(2)
    # List of heroku required variables, any variable with a None value
    # the user will be prompt for input.
    heroku_settings = {
        'DJANGO_SETTINGS_MODULE': '{{ project_name }}.settings.production',
        'SECRET_KEY': _get_secret_key(),
        'AWS_KEY': None,
        'AWS_SECRET': None,
    }
    for key, value in heroku_settings.items():
        if filter(lambda x: key in x, response_list):
            print yellow('Skipping existing %s value.' % key)
            continue
        if value is None:
            value = raw_input("Input value for %s: " % key)
        print green('Setting up %s value.' % key)
        local("heroku config:set %s='%s'" % (key, value))
    addons = local('heroku addons', capture=True).splitlines()
    if filter(lambda x: 'heroku-postgresql' in x, addons):
        print yellow('Existing heroku-postgresql installation found')
    else:
        print yellow('Adding heroku development database.')
        local('heroku addons:add heroku-postgresql:dev')
