
# Todos

## Wordpress Maintenance

- Copy a dev site from the production
  - Copy docroot from prod to dev
  - Change the owner and permissions of the directory
  - Create a MySQL dump on dev
  - Create a new DB from the dump
  - Create a new DB user on dev MySQL
  - Grant privileges to the new user
  - Changed the DB host in wp-config.php
  - Create a virtualhost in sites-available
  - Create a symlink in sites-enabled
  - Check httpd.conf syntax
  - Restart apache

- Replace wordpress domain name

- Update DB host, name, user, password
- Bulk update DB host
- Regenerate keys and salts
- Toggle the debug mode
- Search and replace database contents
- Update a plugin
- Backup/Restore a plugin
- Update all the plugins
- Backup/Restore all the plugins
- Update a theme
- Backup/Restore a theme

## WP-CLI

- Install WP-CLI if it is not installed
- Update WP-CLI

## PHP

- Set up Remi repo
- Install PHP and PHP modules
- Update PHP and PHP modules
- List installed PHP modules

## MySQL

- Restore MySQL database from a specified dump
- Make MySQL dumps for all the sites on a specified machine 
- Restore all the MySQL databases on a specified machine

## EC2

- Create a new EC2 instance that is configured for production
- Create a new EC2 instance that is configured for development
- Stop an EC2 instance
- Create a snapshot

## S3

- Copy/Sync files to S3
- Delete old files on S3

## Apache

- Create a virtual host
- Enable/Disable a virtual host
- Create a self signed certificate

## Redhat

- Install yum-plugin-security if not installed # Only for RH6
- List available security updates
- Install all security updates

## Lets's Encrypt

- Install certbot
- Generate cert
    - Authenticate the ownership
    - Get the certificate
    - Verify the certificate
  
