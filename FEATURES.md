
# PLAYBOOKS Features

## Wordpress Maintenance

- Get all the Wordpress configurations from all servers in production and store locally (get-all-wp-configs)

  ```bash
  # Run get-all-virtualhosts before this
  $ ansible-playbook playbooks/get-all-wp-configs.yml
  ```

## Apache

- Get all the virtual host information from all servers in production and store locally (get-all-virtualhosts)

  ```bash
  $ ansible-playbook playbooks/get-all-virtualhosts.yml
  ```

## MySQL

- Make a MySQL dump for a specified site (dump-mysql-db)

  ```bash
  # Run get-all-virtualhosts and get-all-wp-configs before this
  $ ansible-playbook playbooks/dump-mysql-db.yml -e srchost=<SRCHOST> -e subd=<SUBDOMAIN>
  ```

## Redhat

- Install MySQL-python connector (install-mysql-connector)

  ```bash
  $ ansible-playbook playbooks/install-mysql-connector.yml
  ```


