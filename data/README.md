GEFAK NFL
========================================================================

Gefak NFL for replacing Wincard

GEFAK NFL ist ein Tool damit die GEFAK (Familien Ausgleichskasse) Kinderzulagen, Arbeitgeber kontrollen etc. im Kanton Basel-Land durchführen kann.


Setting up everything
---------------------

### Prerequisites

Install the iwf tools

    https://git.iwf.io/docker/iwf-local-dev/-/blob/main/README.md

### Project setup for developers

a) run the script to copy the initial files. Adjust the copied files to your needs.

    ./bin/init_project.sh

b) (Optional, if you have one) Grab an initial database dump from some system and put it into
docker/run/data/dockerinit.d/mysql/.

    iwf server dbdump dev gefaknfl --dumpfile=docker/run/data/dockerinit.d/mysql/gefaknfl.sql.gz

c) build the fpm container

    iwf stack build

During the setup you need to enter your docker credentials. Please have
them at hand.

d) generate local cert

    iwf cert create

e) start the stack

    iwf stack start

This process takes some time to finish. Once it's finished, scripts are starting inside the docker
containers to install dependencies, assets, clearing cache, ...

To watch the status you can use `iwf stack logs -f`.
To watch the running containers you can use `iwf stack ps`.

f) run yarn (maybe in a second terminal tab)

    iwf yarn dev

g) Test if you can access the application

    iwf launch

h) setup PhpStorm for testing: see https://iwf-web-solutions.atlassian.net/l/cp/LXzD31ui


Starting the project
---------------------

a) start the stack

    iwf stack start

To watch the status you can use `iwf stack logs -f`.
To watch the running containers you can use `iwf stack ps`.

b) run yarn (maybe in a second terminal tab)

    iwf yarn dev

c) Test if you can access the application

    iwf launch

A) Creating test data
----------------------------------

#### loading the fixtures (optional)

    iwf symfony console doctrine:fixtures:load

B) Next steps
----------------------------------

You can access the online API documentation (in dev environment only)
at [http://gefaknfl.test/api/doc](http://gefaknfl/api/doc)

There is no "su"-user in fpm-container anymore. If you need root-privileges, login with root:

    docker exec -ti -uroot gefaknfl-fpm bash

C) Run yarn
-----------
use yarn to compile react code

    iwf yarn dev


PHP Stan
-----------
PHP Stan is a static analysis tool for PHP. It will check the code for errors and potential problems.

Basic configuration is in the file `phpstan.neon`.


### Run PHP Stan
To run PHP Stan, use the following command:

    iwf shell fpm
    phpstan

#### Commands for PHP Stan
The commands can be found on the [PHP Stan website](https://phpstan.org/user-guide/command-line-usage).

### Baseline
Basic information about the baseline can be found on the [PHP Stan website](https://phpstan.org/user-guide/baseline).

#### Create a baseline
This will create a baseline file in the root of the project.
This file will be used to compare the current code with the code in the baseline.
The baseline file will be used to ignore errors that are already in the code.

    iwf shell fpm
    phpstan analyse --generate-baseline

Using Sedex locally
-----------
https://iwf-web-solutions.atlassian.net/wiki/spaces/GEFAKNFL/pages/70746116/Sedex-Client#Lokaler-Betrieb-(f%C3%BCr-devs)

Using S3 locally
----------------

We have a s3 local storage in our stack we could use to save files.
The local S3 Admin can be found on https://minio.gefaknfl.test (Default credentials: minio/minio123, can be changed in your stack)