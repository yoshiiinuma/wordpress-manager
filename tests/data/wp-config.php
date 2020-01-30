<?php
/**
 * The base configurations of the WordPress.
 *
 * This file has the following configurations: MySQL settings, Table Prefix,
 * Secret Keys, WordPress Language, and ABSPATH. You can find more information
 * by visiting {@link http://codex.wordpress.org/Editing_wp-config.php Editing
 * wp-config.php} Codex page. You can get the MySQL settings from your web host.
 *
 * This file is used by the wp-config.php creation script during the
 * installation. You don't have to use the web site, you can just copy this file
 * to "wp-config.php" and fill in the values.
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('WP_CACHE', true); //Added by WP-Cache Manager
define( 'WPCACHEHOME', '/var/www/html/wp-content/plugins/wp-super-cache/' );
define('DB_NAME', 'wordpress_database');

/** MySQL database username */
define('DB_USER', 'wordpress_user');

/** MySQL database password */
define('DB_PASSWORD', 'wordpress_pass');

/** MySQL hostname */
define('DB_HOST', '127.0.0.1');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
define('SECURE_AUTH_KEY',  'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB');
define('LOGGED_IN_KEY',    'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC');
define('NONCE_KEY',        'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD');
define('AUTH_SALT',        'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE');
define('SECURE_AUTH_SALT', 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF');
define('LOGGED_IN_SALT',   'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG');
define('NONCE_SALT',       'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each a unique
 * prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_prefix_';

/**
 * WordPress Localized Language, defaults to English.
 *
 * Change this to localize WordPress. A corresponding MO file for the chosen
 * language must be installed to wp-content/languages. For example, install
 * de_DE.mo to wp-content/languages and set WPLANG to 'de_DE' to enable German
 * language support.
 */
define('WPLANG', '');

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 */
define('WP_DEBUG', true);
define('WP_DEBUG_DISPLAY', false);
define('WP_DEBUG_LOG', true);

/* Disables all core updates, including minor and major: */
define( 'WP_AUTO_UPDATE_CORE', false );

define('FORCE_SSL_ADMIN', false);
//if ($_SERVER['HTTP_X_FORWARDED_PROTO'] == 'https')
//       $_SERVER['HTTPS']='on';

/* True IP from behind a proxy */
// $_SERVER['REMOTE_ADDR'] = preg_replace('/^([^,]+).*$/', '\1',
//         $_SERVER['HTTP_X_FORWARDED_FOR']);

/* Multisite */
define('WP_ALLOW_MULTISITE', true);

define('MULTISITE', true);
define('SUBDOMAIN_INSTALL', false);
$base = '/';
define('DOMAIN_CURRENT_SITE', 'odo.example.com');
define('PATH_CURRENT_SITE', '/');
define('SITE_ID_CURRENT_SITE', 1);
define('BLOG_ID_CURRENT_SITE', 1);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
