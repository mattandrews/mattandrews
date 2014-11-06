from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['matt@162.243.234.162:25000']

def commit():
    with hide('warnings'):
        with settings(warn_only=True):
            msg = prompt("commit message: ")
            local('git add . && git commit -m "%s"' % msg)

def push():
    local("git push")

def prepare_deploy():
    commit()
    push()

def deploy():
    prepare_deploy()
    code_dir = '/var/www/mattandrews/matt'
    with cd(code_dir):
        run("git pull")
        with prefix('source ve/bin/activate'):
            run("pip install -r requirements.txt")
        sudo("supervisorctl restart matt")
        # todo: cachebust here?
