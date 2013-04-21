.. {% comment %}
Django template plus
--------------------

Django template plus allows you to easily bootstrap a new Django project locally using vagrant and remotely using Heroku.

By using this you should be able to sandbox and reasonably replicate Heroku environment to run your application.


Creating a new project
----------------------

Please note that requires ``Django`` and ``django-startproject-plus`` installed.

Make sure you create the heroku app **before** running the command.

Spawn the project by running this command where the project will be living, please note that this doesn't require a checkout of this template, since it can be retrieved from an ``https`` location::

    django-startproject.py PROJECT_NAME --template=https://github.com/alfredo/django-template-plus/archive/master.zip --extra_context='{"project_url": "PROJECT_URL", "heroku_app": "HEROKU_APP", "project_ip": "PROJECT_IP"}' --extension=py,rst,local,yaml,py-dist --name=Procfile


Where:

- ``PROJECT_NAME`` is the project name of your application, must be a valid python variable name. e.g. ``foo``
- ``PROJECT_URL`` is the URL that will be used for the vagrant VM. e.g. ``local-foo.org``
- ``HEROKU_APP`` is the name of the application in heroku. e.g. ``mystic-wind-83``
- ``PROJECT_IP`` is the private network ip used to access the VM. e.g. ``33.33.33.1``


README.rst file template
========================

The following section is part of the template which will appear in the ``README.rst`` file of the project.

.. {% endcomment %}
Project for {{ project_url }}


Setup Heroku
------------

Once the application has been created in Heroku and you are a collaborator.

Setup the settings for the application::

  heroku config:set DJANGO_SETTINGS_MODULE={{ project_name }}.settings.production


Add a secret key for the project::

  heroku config:set SECRET_KEY=


Add AWS credentials to be used for the static files::

  heroku config:set AWS_KEY=
  heroku config:set AWS_SECRET=



Add the heroku remote::

    git remote add heroku git@heroku.com:{{ heroku_app }}.git

Deploy the application to heroku::

    git push heroku master




Bootstraping the VM
-------------------

Before starting the VM you require ``vagrant`` and another provider ``virtualbox`` has no cost.

Start the VM by runnning from the root of the repository::

  vagrant up

After the the VM has been installed and provisioned the application should be available at http://{{ project_ip }}

There are a few other commands that can help you to work with the VM.

Add the following line to ``/etc/hosts`` to access the VM via http://{{ project_url }} ::

    {{ project_ip }}    {{ project_url }}


Add an ssh config entry for this project, so you can access the VM with ``ssh {{ project_name }}::

    vagrant ssh-config --host {{ project_name }} | sed -e '$a\' | tee -a ~/.ssh/config
