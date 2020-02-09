#title          : Performance Test Agent
#description    : An agent to run test scripts from ScriptHome directory and serve test results
#author         : Regin Vinny
#license        : GNU GENERAL PUBLIC LICENSE Version 3
#date           : 2019-12-25
#version        : 1.0
#usage          : export scriptHome=<script home path>
#                 python perftest-agent.py
#notes          : Arbitrary command execution is blocked


#!/usr/bin/python

import threading,subprocess,SimpleHTTPServer,SocketServer,os
from datetime import datetime

PERFTEST_AGENT_PORT_NUMBER = 7008
FILE_SERVER_PORT = 7009
WEB_DIR=os.environ['scriptHome'] #Change to the script home directory
LOG_DIR=WEB_DIR # writes log file to scriptHome
#LOG_DIR=os.path.dirname(os.path.abspath(__file__)) # activate to write log to performance test agent path


def run_perftest_agent():
    from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer


    class myHandler(BaseHTTPRequestHandler):
        
        def _set_headers(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()   

        def _html_Man(self):
            content = """
            <!DOCTYPE html><html><head></head><body> 
            <h1>Performance Test Agent</h1> 
            <h2>Usage:</h2> 
            <p><b>Invoke Test shell script : </b> curl -d "script-path/script.sh http://[IP or DNS]:"""+str(PERFTEST_AGENT_PORT_NUMBER)+"""</p>
            <p><b>Clear logs (Rotate) : </b> curl -d "clear" http://[IP or DNS]:"""+str(PERFTEST_AGENT_PORT_NUMBER)+"""</p>
            <p><b>Fetch test results : </b> curl http://[IP or DNS]:"""+str(FILE_SERVER_PORT)+"""</p>
            <p><b>Note: </b>Target sh file must be present in the Script Home directory</p></body></html>
            """.format()
            return content.encode("utf8") 
   
        def _custom_response(self,message):
             self._set_headers()
             # Send the html message
             content = message.format()
             self.wfile.write(content.encode("utf8"))             
             return 


        #Handler for the GET requests
        def do_GET(self):
            self._set_headers()
            # Send the html message
            self.wfile.write(self._html_Man())
            return
        
        def do_HEAD(self):
            self._set_headers()

        def do_POST(self):
            self._set_headers()
            #Read post body
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            #print(post_body.decode("utf-8"))
            if (self.cmdCheck(post_body)):
                print ("character allowed")
                self._convertToOSCmd(self.path,post_body)

        def cmdCheck(self,cmd):
            arr = ['&', '&&', '|', '||', ';','\\n','0x0a','`']            
            if any(c in cmd for c in arr):
                print ("character not allowed")
                self._logger("ALERT!!!! UNSUPPORTED CHARACTER BLOCKED IN INCOMING COMMAND :" + cmd)
                self._custom_response("ERROR: UNSUPPORTED CHARACTER(S) IN THE COMMAND [& | ; \\n 0x0a `]")
                return False
            return True


        def _convertToOSCmd(self, path, cmd):
            """ This functions runs OS command
            """
            if (cmd=="clear"):
                self._logRotate()      
            else:
                self._runOSCmd("sh " + WEB_DIR + "/" + cmd +" >> "+ LOG_DIR +"/perftest-agent.log &")                
                    
        def _runOSCmd(self, oscmd):
                """ This function runs OS command
                """
                print(oscmd,": Command to Run")
                self._logger(oscmd)

                #Execute OS command            
                returned_value = subprocess.call(oscmd, shell=True)  # returns the exit code in unix
                print('returned value:', returned_value)

    

        def _logger(self, message):
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
                f=open(""+ LOG_DIR +"/perftest-agent.log", "a+")
                f.write(timestamp + " " + message + "\n" )
        
        def _logRotate(self):
                timestamp=datetime.now().strftime('%Y-%m-%d_%H%M%S')    
                self._runOSCmd("cp "+ LOG_DIR +"/perftest-agent.log "+ LOG_DIR +"/perftest-agent"+timestamp+".log &")
                self._runOSCmd("echo '********* Log rotated ********' > "+ LOG_DIR +"/perftest-agent.log &")

    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PERFTEST_AGENT_PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PERFTEST_AGENT_PORT_NUMBER
    
    #Wait forever for incoming http requests
    server.serve_forever()


def run_fileserver():
    os.chdir(WEB_DIR)
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", FILE_SERVER_PORT), Handler)
    print "Serving at port", FILE_SERVER_PORT
    httpd.serve_forever()

if __name__=='__main__':
    t1 = threading.Thread(target=run_perftest_agent)
    t2 = threading.Thread(target=run_fileserver)
    t1.start()
    t2.start()