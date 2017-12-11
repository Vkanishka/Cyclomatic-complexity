from flask import request
import shutil
from dask.distributed import Client
import time
from flask import Flask
from git import Repo
import os
import subprocess

app = Flask(__name__)
client = Client('127.0.0.1:8786')


def cyclomatic_complexity_analyzer(p):
    raw_complexity = subprocess.Popen(["radon raw " + p + " -s -j"], stdout=subprocess.PIPE, shell=True,
                                      executable='/bin/bash')
    cyclomatic_complexity = subprocess.Popen(["radon cc " + p + " -s -j"], stdout=subprocess.PIPE, shell=True,
                                             executable='/bin/bash')
    (raw_complexity_output, err) = raw_complexity.communicate()
    (cyclomatic_complexity, err1) = cyclomatic_complexity.communicate()
    return raw_complexity_output + cyclomatic_complexity


def complexity_with_distributed(git_files):
    s = time.time()
    result = client.map(cyclomatic_complexity_analyzer, git_files)
    r = client.gather(result)
    print("Time %s" % (time.time() - s))
    return r


def creation_of_filelist(git_files, dir, filenames):
    for filename in filenames:
        if filename.endswith('.py'):
            git_files.append(str(os.path.join(dir, filename).encode('ascii', 'ignore')))


@app.route('/to_calculate_complexity')
def calc_cyclomatic_complexity():
    gitlink = request.args.get('gitlink')
    name = (gitlink.split('/')[-1]).split('.')[0]
    p = "/gitfolder/" + name
    Repo.clone_from(gitlink, p)

    if os.path.isdir(p + "/.git"):
        shutil.rmtree(p + "/.git")
    p = os.path.expanduser(p)
    git_files = []

    if os.path.isdir(p):
        os.path.walk(p, creation_of_filelist, git_files)

    r = complexity_with_distributed(git_files)

    if os.path.isdir(p):
        shutil.rmtree(p)

    return "correct"


if __name__ == '__main__':
    app.run()