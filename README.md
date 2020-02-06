# Ansible Playbooks and Modules for Wordpress Maintenance

## Setup

```bash
# pipenv will create the virtual env (.venv) in ther project root

$ echo 'export PIPENV_VENV_IN_PROJECT=1' >> .bashrc
$ source .bashrc
```

## Install

```bash
$ git clone https://github.com/yoshiiinuma/wordpress-manager.git
$ cd wordpress-manager

$ pip install pipenv

$ pipenv install
# or to install both develop and default packages
$ pipenv install --dev
```

## Run Tests

```bash
$ pipenv shell

$ pytest tests
```

## Run Ansible Playbook

```bash
$ pipenv shell

$ ansible-playbook playbooks/<playbook.yml>

# Pass variables
$ ansible-playbook playbooks/<playbook.yml> -e '{"key1":"val1","key2":"val2"}'

# Limit hosts
$ ansible-playbook playbooks/<playbook.yml> -l 'h1,h2'
```

## Run Module as Ansible Command

```bash
$ pipenv shell

$ ansible <host> -m <module-name>

# Pass argument
$ ansible <host> -m <module-name> -a 'key=val'
```

## Run Module with Python

```bash
$ pipenv shell

$ python -m lib/<module-name> args/<args-for-module.json>
```
