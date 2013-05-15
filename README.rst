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
=============================

This project is capable to be run in Heroku and locally using Vagrant and one of its providers with puppet.


Running in  Heroku
------------------

In order to run a new instance of this project in Heroku you will need:

- A heroku account and an empty app for this project to live in.
- An AWS S3 account and credentials pair.
- Python fabric installed.

Once these dependencies have been meet, the heroku remote should be added to the project::
  git init
  git remote add production git@heroku.com:{{ heroku_app }}.git
  git add .
  git commit -a -m "Initial commit."

Please note that the alias ``production`` is used, this will come in-handly later when multiple heroku environments are used for this project

Next the Heroku environment for the application to live in must be configured, this can be achieved by running the following fabric command::

  fab setup_heroku

This command will add a ``DJANGO_SETTINGS_MODULE``, a ``SECRET_KEY`` environment variable. It will also need a ``AWS_KEY`` and ``AWS_SECRET`` to access the ``S3`` storage for the assets.

The last step of the fabric command will provision a ``heroku-postgresql:dev`` if a postgresql server hasn't been added to the heroku app.

These variables were added as an environment variable since they are very sensitive and that should help to open source your app, if you should decide to do so.

Finnaly  don't forget to create the bucket in AWS for the application static files to live in::

  static.{{ project_url }}

Once all these steps have been met the application should be able to be deployed with::

   fab production deploy

And the aplication will be available at http://{{ heroku_app }}.herokuapp.com/


Running locally
---------------

In order to run the application locally you will require Vagrant and a provisioner installed in your local machine (VirtualBox being the easiest provisioner you can get hold of).

Once installed you can start the VM by runnning from the root of the repository, the following command::

  vagrant up

After the VM has been installed and provisioned the application should be available at http://{{ project_ip }}, a port forwarding from 80 to 8000 has been setup so you should be able to access http://localhost:8000 as well.

There are a few other commands that can help you to interact better with the VM.

Add the following line to ``/etc/hosts`` to access the VM via http://{{ project_url }} ::

    {{ project_ip }}    {{ project_url }}


Add an ssh config entry for this project, so you can access the VM with ``ssh {{ project_name }}::

    vagrant ssh-config --host {{ project_name }} | sed -e '$a\' | tee -a ~/.ssh/config
