import os, sys, requests, json
import subprocess
import CC
import lizard

if __name__ == '__main__':

    ip = "127.0.0.1"     # providing the ip and port number to the server
    port = "8080"
    reqURL = 'http://' + ip + ':' + port
    register_url = reqURL + '/lodge_slave'
                                     # req complexity from the worker
    complexity_url = reqURL + '/complexity_from_slave'
    files_checked = 0

    reg_response = requests.get(register_url)
    print reg_response.text

