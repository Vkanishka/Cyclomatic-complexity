from flask import Flask
from git import Repo
from flask import request
import shutil
import os
import subprocess
import time
from dask.distributed import Client 

app = Flask(__name__)
client = Client('127.0.0.1:8786')


def creation_of_filelist(file_list, dir, filenames):
    for filename in filenames:
        if filename.endswith('.py'):
            file_list.append(str(os.path.join(dir, filename).encode('ascii', 'ignore')))


def cyclomatic_complexity_analyzer(path):
    raw_complexity = subprocess.Popen(["radon raw " + path + " -s -j"], stdout=subprocess.PIPE, shell=True,
                                      executable='/bin/bash')
    cyclomatic_complexity = subprocess.Popen(["radon cc " + path + " -s -j"], stdout=subprocess.PIPE, shell=True,
                                             executable='/bin/bash')
    (raw_complexity_output, err) = raw_complexity.communicate()
    (cyclomatic_complexity, err1) = cyclomatic_complexity.communicate()
    return raw_complexity_output + cyclomatic_complexity

def cyclo_complexity_with_no_distributed(file_list):
    start_time = time.time()
    for path in file_list:
        cyclomatic_complexity_analyzer(path)
    print("--- %s seconds ---" % (time.time() - start_time))

def complexity_with_distributed(file_list):
     start_time = time.time()
     A = client.map(cyclomatic_complexity_analyzer, file_list)
     print client.gather(A)
     print("--- %s seconds looooo ---" % (time.time() - start_time))


@app.route('/to_calculate_complexity')
def calc_cyclomatic_complexity():
    file_list = []
    url = request.args.get('url')
    name = (url.split('/')[-1]).split('.')[0]
    print name
    path = "/repos/" + name
    Repo.clone_from(url, path)
    if os.path.isdir(path + "/.git"):
        shutil.rmtree(path + "/.git")
    path = os.path.expanduser(path)
    if os.path.isdir(path):
        os.path.walk(path, creation_of_filelist, file_list)

    complexity_with_distributed(file_list)
    cyclo_complexity_with_no_distributed(file_list)
    return "success"


if __name__ == '__main__':
    app.run()
