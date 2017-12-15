# Cyclomatic-complexity

for a given repository cyclomatic complexity is analysed 

IDE-  Pycharm

--> Dependencies

--> python 2.7 is used for this program

--> Lizard 1.13.0 is a Python package to calculate the cyclomatic complexity

used Flask which is an REST API

used Radon tool that computes various metrics from the source code.
like Cyclomatic complexity

used methodology
--> Dask which is an parallel computing library.
--> user customised master-slave architecture.

# process starts with Terminal

--> Dask-scheduler 

--> Dask-worker 192.168.1.15:8786 ( includes IP and Port number )
after sucessfully Registered to:    tcp://192.168.1.15:8786

then we RUN the file Cyclomatic Complexity file [ CC ]

* cyclomatic complexity is analysed under dask server
* link is requested for analysing the complexity, Link is taken from any random github repository
* the repository which is taken from github is 

gitlink : https://github.com/Vkanishka/ChatApp.git

* Dask Api was used to perform distributed computing in python
* calc_cyclomatic_complexity

          /to_calculate_complexity
 
 
* open the browser tab to proceed with the process

     link : http://127.0.0.1:5000/to_calculate_complexity?gitlink=https://github.com/Vkanishka/ChatApp.git

      output :[{"/gitfolder/ChatApp/Server.py": [{"name": "check_msg", "col_offset": 4, "rank": "C", "classname": "ChatUsersThreadClass", "complexity": 16, "closures": [], "endline": 213, "type": "method", "lineno": 153}
      
      
  ** run the dask master and Dask slave files
    
slave side :
* providing the ip and port number to the server
   
    ip = "127.0.0.1"      == IP of the Server
    
    port = "8786"         == port of the dask server
    
    reqURL = 'http://' + ip + ':' + port 
 
* by default values : IP (localhost): 127.0.0.1
                      Port: 8786
                      
    
  Master Side :
* server manager node which handles all the stuff like 
  - slave count
  - start time
  - file complexity list
  - path
  - file list
  - total number of file

* Registering the slave to the Master
* work by server manager node
* to get the complexity from slave
    * Requesting a file path
    * Shows no. of files analysed 
    * Shows Cyclomatic complexity of the Repository.
    
