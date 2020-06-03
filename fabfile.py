# For full fab documentation see:
# http://docs.fabfile.org/en/1.14/api/core/operations.html

from __future__ import with_statement

from datetime import datetime
import time
from fabric.api import *

import os

SUDO_USER_PROD = 'leobreslav'
IP_PROD = '5.63.157.152'
PATH_TO_PROJECT_PROD = './MathProblems'
PATH_TO_VENV_BIN_PROD = 'venv/bin/'

DATABASE_NAME_PROD = 'mathproblems'
DATABASE_USERNAME_PROD = 'leobreslav'

DATABASE_NAME_LOCAL = 'mathproblems'
DATABASE_USERNAME_LOCAL = 'leobreslav'

PATH_TO_MEDIA_PROD = './MathProblems/MathProblems/media'
PATH_TO_MEDIA_LOCAL = 'MathProblems/media'

PATH_TO_DB_BACKUP_LOCAL = 'backup/db'


env.hosts = [SUDO_USER_PROD + '@' + IP_PROD]

# Uncomment to ignore execution errors and continue executing
# See http://docs.fabfile.org/en/1.4.1/usage/execution.html#failure-handling
#
# env.warn_only = True



def start():
    run("sudo systemctl start gunicorn")


def stop():
    run("sudo systemctl stop gunicorn")


def restart():
    run("sudo systemctl restart gunicorn")


def status():
    run("sudo systemctl status gunicorn")


def take_comment():
    m = input('input commit comment:\n')
    return m


def git_push():
    local('git add --all')

    comment = take_comment()

    local('git commit -m "' + comment + '"')
    local('git push')


def deploy():
    # If any issues with ascii errors just add this commands
    # run('export LC_ALL=en_US.UTF-8')
    # run('export LANG=en_US.UTF-8')

    # Push new version to remote repo
    git_push()

    #  Stop gunicorn
    stop()

    with cd(PATH_TO_PROJECT_PROD):
        # get the latest version from master branch
        run('git pull origin master')

        # install requirements
        run(PATH_TO_VENV_BIN_PROD + 'pip3 install -r ./requirements.txt')

        # migrate data
        run(PATH_TO_VENV_BIN_PROD + 'python manage.py migrate')

        # collect static
        run(PATH_TO_VENV_BIN_PROD + 'python manage.py collectstatic')

    # Start gunicorn
    start()


def dump_local_db():
    time_str = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%-M-%S')

    dump_filename = PATH_TO_DB_BACKUP_LOCAL + '/dump_' + time_str + '.sql'

    local('mysqldump --databases ' + DATABASE_NAME_LOCAL + ' > ' + dump_filename + ' -u ' + DATABASE_USERNAME_LOCAL + ' -p')

    return dump_filename


# Dump a prod db with a timestamp
# returns a filename of dump
def dump_prod_db():
    time_str = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')

    dump_filename = 'dump_' + time_str + '.sql'

    run('mysqldump --databases ' + DATABASE_NAME_PROD + ' > ' + dump_filename + ' -u ' + DATABASE_USERNAME_PROD + ' -p')

    return dump_filename


def replace_prod_db(dump_filename):
    run('mysql -u ' + DATABASE_USERNAME_PROD + ' -p ' + DATABASE_NAME_PROD + ' < ' + dump_filename)


def replace_local_db(dump_filename):
    os.system('mysql -u ' + DATABASE_USERNAME_LOCAL + ' -p ' + DATABASE_NAME_LOCAL + ' < ' + dump_filename)
    pass


# This method replaces remote db with local db!
def replace_prod_db_with_local_db():
    # dump local db
    dump_filename = dump_local_db()

    dump_filename_after_upload = 'local_' + dump_filename

    # copy file to server
    put(dump_filename, dump_filename_after_upload)

    # dump prod db
    dump_prod_db()

    # replace prod db with uploaded local db
    replace_prod_db(dump_filename_after_upload)


def replace_local_db_with_prod_db():
    # dump local db
    dump_local_db()

    # dump prod db
    dump_filename = dump_prod_db()

    dump_filename_after_download = PATH_TO_DB_BACKUP_LOCAL +'/dump_'+ dump_filename

    # copy file from server
    get(dump_filename, dump_filename_after_download)

    # replace prod db with uploaded local db
    replace_local_db(dump_filename_after_download)


def download_media():
    # copy files from server
    get(PATH_TO_MEDIA_PROD, PATH_TO_MEDIA_LOCAL)
