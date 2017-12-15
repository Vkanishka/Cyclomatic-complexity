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


