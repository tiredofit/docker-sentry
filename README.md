# hub.docker.com/tiredofit/sentry

# Introduction

Dockerfile to build a [Sentry](https://www.sentry.io) container image.

* This Container uses Debian Stretch as a base which includes [s6 overlay](https://github.com/just-containers/s6-overlay) enabled for PID 1 Init capabilities, [zabbix-agent](https://zabbix.org) based on 3.4 Packages for individual container monitoring, Cron also installed along with other tools (bash,curl, less, logrotate, mariadb-client, nano, vim) for easier management.

* LDAP Functionality included
* SSO Functionality included

[Changelog](CHANGELOG.md)

# Authors

- [Dave Conroy](http://github/tiredofit/)

# Table of Contents

- [Introduction](#introduction)
    - [Changelog](CHANGELOG.md)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
    - [Database](#database)
    - [Data Volumes](#data-volumes)
    - [Environment Variables](#environmentvariables)   
    - [Networking](#networking)
- [Maintenance](#maintenance)
    - [Shell Access](#shell-access)
   - [References](#references)

# Prerequisites

This image assumes that you are using a reverse proxy such as [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy) and optionally the [Let's Encrypt Proxy Companion @ https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion](https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion) in order to serve your pages. However, it will run just fine on it's own if you map appropriate ports.

You will need a Redis server and also a Postgresql 9.6 DB Server


# Installation

Automated builds of the image are available on [Registry](https://hub.docker.com/r/tiredofit/sentry) and is the recommended method of installation.


```bash
docker pull /tiredofit/sentry:(imagetag)
```

The following image tags are available:

* `latest` - Most recent release of Sentry w/most recent Debian Stretch

# Quick Start

* The quickest way to get started is using [docker-compose](https://docs.docker.com/compose/). See the examples folder for a working [docker-compose.yml](examples/docker-compose.yml) that can be modified for development or production use.

* Set various [environment variables](#environment-variables) to understand the capabilities of this image.
* Map [persistent storage](#data-volumes) for access to configuration and data files for backup.

# Configuration

### Data-Volumes

The following directories are used for configuration and can be mapped for persistent storage.

| Directory | Description |
|-----------|-------------|
| `/etc/sentry` | If you would like to use your own configuration, expose this folder. |
| `/var/lib/sentry/files` | Sentry Data |

### Database

An external Postgresql Database is required for using this image.
Additionally, you must have access to a Redis Server

### Environment Variables

Along with the Environment Variables from the Base image (tiredfoit/debian:stretch), below is the complete list of available options 
that can be used to customize your installation.

| Parameter | Description |
|-----------|-------------|
| `DB_HOST` | Name of Postgresql Container e.g. `sentry-db`|
| `DB_PORT` | Port of Postgresql Container Default `5432`|
| `DB_NAME` | Name of Postgresql Database |
| `DB_USER` | Username for Postgresql Database |
| `DB_PASS` | Username for Postgresql Database |
| `RABBITMQ_HOST` | RabbitMQ Hostname if utilized |
| `RABBITMQ_USER` | Username for Postgresql Database|
| `RABBITMQ_PASS` | Password for RabbitMQ if used |
| `RABBITMQ_VHOST` | RabbitMQ Vhostname if used |
| `REDIS_HOST` | Redis Server Container e.g. `sentry-redis` |
| `REDIS_PASS` | Redis Password if used |
| `REDIS_PORT` | Redis Port number Default `6379` |
| `REDIS_DB` | Redis DB Number if required |
| `MEMCACHED_HOST` | Memcached Container name e.g. `sentry-memcached` |
| `MEMCACHED_PORT` | Memcached Port Default `11211` |
| `SERVER_EMAIL` | Default Server FROM address |
| `SMTP_HOST` | SMTP Server Hostname |
| `SMTP_PORT` | SMTP Server Port |
| `SMTP_USER` | Username for SMTP Server if used |
| `SMTP_PASS` | Password for SMTP Server if used |
| `SMTP_USE_TLS` | Use TLS with SMTP `True` or `False` Default `False` |
| `ENABLE_EMAIL_REPLIES` | Enable Email Replies `True` or `False` Default `False` |
| `SMTP_HOSTNAME` | What is the hostname you with to advertise yourself as .. |
| `MAILGUN_API_KEY` | Mailgun API key if used |
| `SINGLE_ORGANIZATION` | Enable Single Organizations `True`/`False` Default `True` |
| `SECRET_KEY` | 32 character long secret key |
| `GITHUB_APP_ID` | If using Github, enter AppID |
| `GITHUB_API_SECRET` | API for Github |
| `BITBUCKET_CONSUMER_KEY` | If using Bitbucket, enter Key |
| `BITBUCKET_CONSUMER_SECRET` | Bitbucket Key |

LDAP / SSO Functionality:


| Parameter | Description |
|-----------|-------------|
| `LDAP_ENABLE` | Enable Ldap Support `TRUE`/`FALSE` Default `FALSE` |
| `LDAP_BASE_DN` | LDAP Base DN e.g. `dc=example,dc=com` |
| `LDAP_BIND_USER` | Bind user e.g. `cn=admin,dc=example,dc=com` | 
| `LDAP_BIND_PASSWORD` | LDAP Bind Password |
| `LDAP_URI` | URI of LDAP Server e.g. `ldap://ldap.example.com` |
| `LDAP_DOMAIN` | @suffix for members who don't have `mail` attribute e.g. `example.com` |
| `LDAP_FIND_GROUP_PERMS` | Find Group Permisions `True`/`False` Default `True` |
| `LDAP_CACHE_GROUPS` | Cache Groups `True`/`False` Default `True`
| `LDAP_GROUP_CACHE_TIMEOUT` | Group Cache Timeout in seconds Default: `3600` |
| `LDAP_UID_ATTR` | UID attribute Default `uid` |
| `LDAP_NAME_ATTR` | Name Attribute Default `cn` |
| `LDAP_MAIL_ATTR` | Mail Attribute Default `mail` |
| `LDAP_USER_SCOPE` | User Search scope Default `(mail=%(user)s)` |
| `LDAP_GROUP_SCOPE` |  Group Search Scope Default `(objectClass=groupOfUniqueNames)` |
| `LDAP_ORGANIZATION_NAME` | Organization Name to place members in Default `sentry` |
| `LDAP_AUTO_ADD_ROLE_TYPE` |  Role type auto added users are assigned Default `member`
| `LDAP_AUTO_ADD_GLOBAL` |  Autocreated users should be granted global access to org Default `False`


### Networking

The following ports are exposed.

| Port      | Description |
|-----------|-------------|
| `9000`    | Sentry UWSGI|

# Maintenance
#### Shell Access

For debugging and maintenance purposes you may want access the containers shell. 

```bash
docker exec -it (whatever your container name is e.g. sentry) bash
```

# References

* https://www.sentry.io


