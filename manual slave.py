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

    while True:
        work_data = requests.get(complexity_url)
        json_data = json.loads(work_data.text)
        file_path = json_data['status']          # getting url path from master
        print ("" + str(file_path))
        if file_path == -2:
            print("messaging  the server")    # sending message to server
            break
        else:
            if file_path == -1:
                print("work done ")    # message response as work completed
                break

        Complexity_value_radon = lizard.analyze_file(file_path).average_cyclomatic_complexity

        print("Complexity analysis report of the file:" + str(Complexity_value_radon))
        average_complexity = float(Complexity_value_radon)
        master_response = requests.post(complexity_url,
                                        json={'f_path': file_path, 'complexity': average_complexity})
        files_checked += 1
print("Total Files Checked: ", files_checked)

