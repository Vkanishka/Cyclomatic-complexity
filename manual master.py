from flask import Flask  # To implement rest service
import time
import CC
from flask import request
from flask import jsonify
import os
import shutil

app = Flask(__name__)  # Rest service


class server_manager_node:     # server manager for handling the stuff
    def __init__(self):
        self.c_s_c = 0        # current slave count
        self.slave_count = 1
        self.start_time = 0.0
        self.f_complexity_list = []    # file complexity list
        file_list, path = CC.git_expand("https://github.com/Vkanishka/ChatApp.git")
        self.path = path
        self.file_list = file_list
        self.total_file = len(self.file_list)
        print("number count of commits: {}".format(self.total_file))

# a
@app.route('/lodge_slave', methods=['GET'])      # Registering the slave to the master
def lodge_slave():
    print "-- lodging the slave to the master --"
    server_manager_node.c_s_c += 1
    if server_manager_node.c_s_c == server_manager_node.slave_count:
        server_manager_node.start_time = time.time()
    return "lodged"


# c
@app.route('/complexity_from_slave', methods=['POST'])   # to get the complexity from slave
def complexity_from_slave():
    f_path = request.args.get('f_path')  # requesting a file path
    code_complexity_req = request.json
    f_path= code_complexity_req['f_path']
    code_complexity= code_complexity_req['complexity']
    print code_complexity
    server_manager_node.f_complexity_list.append({'f_path': f_path, 'complexity': code_complexity})
    if len(server_manager_node.f_complexity_list) == server_manager_node.total_file:
        time_end = time.time() - server_manager_node.start_time
        print("Ext Time taken: ", time_end)
        print("No. of files analyzed:"+ str(len(server_manager_node.f_complexity_list)))  # shows no. of files analysed
        print server_manager_node.f_complexity_list
        average_complexity = 0
        for x in server_manager_node.f_complexity_list:
            if x['complexity'] > 0:
                average_complexity += x['complexity']
            else:
                print("No files to be analyzed")
        average_complexity = average_complexity / len(server_manager_node.f_complexity_list)
        print("Cyclomatic Complexity of the Repository: ", average_complexity)  # shows Cyclometric complexity of the rep.

                                                    # Remove the git cloned folder after use
        if os.path.isdir(server_manager_node.path):
            shutil.rmtree(server_manager_node.path)

    return jsonify({'success': True})

# b
@app.route('/complexity_from_slave', methods=['GET'])
def get_work():
    if server_manager_node.c_s_c < server_manager_node.slave_count:
        time.sleep(0.1)
        return jsonify({'status': -2})
    if len(server_manager_node.file_list) == 0:
        return jsonify({'status': -1})
    f_path = server_manager_node.file_list[0]
    del server_manager_node.file_list[0]
    print "Sending work to slave:"+f_path
    return jsonify({'status': f_path})

if __name__ == '__main__':
    server_manager_node = server_manager_node()
    app.run(port =8080)


