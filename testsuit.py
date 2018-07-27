'''
Created on 24 Jun 2015

@author: Satish
'''
import time
from devicemanager import *
from Tkinter import *
import operator
import webbrowser
from operator import itemgetter
import collections

'''Class test suite consisting of test cases as member funtions
   device manager member functions used to establish socket
   member variables are initialised in constructor.  
'''
 
class testsuitedm():
    
    #constructor
    def __init__(self):
        self.dm = devicemanager()
        self.setup_connect = True
        self.tcresults = collections.OrderedDict()
        self.device_address = "0x1234"
        self.connect_handle = ""
        self.result = ""
        self.root = Tk()
    
    #function to establish socket
    #defined in class device manager    
    def device_setup(self):
        self.dm.setup("127.0.0.1", 2800)
        res = self.dm.connect()
        if res == 1:
            self.setup_connect = True
        else:
            self.setup_connect = False
    
    ''' test case1 to verify DM initialisation
        check for connection
        check for return message
    '''
    def tc1_dminitialize(self):
        
        if self.setup_connect:
            cmd = "INIT\n"
            self.dm.sendcommand(cmd)
            val = self.dm.recievedata()
            try:
                assert(val.find("OK") != -1), "Pass"
                self.result = "Pass"
            except AssertionError:
                reason = "  Initialisation failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result 
    
    ''' tc2 to verify DM accepts new connections
        check for socket connection
        send CONNECT with device address
        check for return message
    '''
            
    def tc2_establishConnection(self):
        time.sleep(2)
        self.tc1_dminitialize()
        if self.setup_connect:
            cmd = "CONNECT" + ' ' + self.device_address + "\n"
            self.dm.sendcommand(cmd)
            val = self.dm.recievedata()
            if val.find("ERROR") != -1:
                reason = "  Connection failed"
                self.result = "Fail" + reason
            else:
                self.connect_handle = val.rstrip()
                self.result = "Pass"
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result 
    
    ''' tc3 to verify dm reject invalid address
        send CONNECT with invalid address
    '''
    def tc3_establishConn_invalid_addr(self):
        
        invalid_address = "1232"
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            cmd = "CONNECT" + ' ' + invalid_address + "\n"
            self.dm.sendcommand(cmd)
            val = self.dm.recievedata()
            if val.find("ERROR") != -1:
                self.result = "Pass"
            else:
                reason = "Invalid Address accepted by DM"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result 
    
    ''' tc4 to verify dm accepts decimal value address
        send CONNECT with decimal address covert from hex
        Verify for ERROR
    '''
    def tc4_establish_connection_addr_integer(self):
        
        address_decimal = int(self.device_address, 0)
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            cmd = "CONNECT" + ' ' + str(address_decimal) + "\n"
            self.dm.sendcommand(cmd)
            val = self.dm.recievedata()
            if val.find("ERROR") != -1:
                reason = "Invalid Address accepted by DM"
                self.result = "Fail" + reason
            else:
                self.result = "Pass"
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result 

    ''' tc5 to verify dm rejects the for existing connection
         call member function tc3 twice with delay
    '''
    def tc5_establish_connection_exists_devmanager(self):
        
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            time.sleep(5)
            val = self.tc2_establishConnection()
            if val.find("ERROR") == -1:
                self.result = "Pass"
            else:
                reason = "Already existing Address accepted by DM"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result 
    
    ''' tc6 and tc7 verify that device manager decodes GET
        Send GET with parameter as parameter_a
    '''
    def tc6_tc7_get_database_para1(self, dbname):
        
        time.sleep(5)
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            cmd = "GET" + ' ' + self.connect_handle + dbname + "\n"
            self.dm.sendcommand(cmd)
            val = self.dm.recievedata()
            if val.find("ERROR") == -1:
                self.result = "Pass"
            else:
                reason = "GET command failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result 
    
    ''' tc7 verify that device manager decodes GET
        Send GET with parameter as parameter_a parameter_b
    '''
    def tc8_get_database_para1_para2(self):
        
        time.sleep(5)
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            cmd = "GET" + ' ' + self.connect_handle + " parameter_a" + " parameter_b" + "\n"
            self.dm.sendcommand(cmd)
            val = self.dm.recievedata()
            if val.find("ERROR") != -1:
                self.connect_handle = val
                self.result = "Pass"
            else:
                reason = "GET command failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        
        return self.result 
    
    def testcase_sendreset(self):
        cmd = "RESET" + "\n"
        self.dm.sendcommand(cmd)
  
    ''' tc6 and tc7 verify that device manager decodes GET
        Send GET with parameter as parameter_a
    '''
    def tc9_get_database_invalid_para1(self):
        time.sleep(5)
        dbname = " parameter1"
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            cmd = "GET" + ' ' + self.connect_handle + dbname + "\n"
            print "cmd", cmd
            self.dm.sendcommand(cmd)
            val = self.dm.recievedata()
            if val.find("ERROR") != -1:
                self.result = "Pass"
            else:
                reason = "GET command failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result 
    
    ''' tc10 verify that device manager decodes 
        multiple GET request
        Value range is set to 15
    '''
    def tc10_multiple_Get_Request(self):
        
        time.sleep(5)
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            for i in range(0, 8):
                cmd = "GET" + ' ' + self.connect_handle + " parameter_a1" + "\n"
                self.dm.sendcommand(cmd)
                time.sleep(1)
                val = self.dm.recievedata()
                if val.find("ERROR") != -1:
                    self.result = "Pass"
                else:
                    reason = " Multiple GET command failed"
                    self.result = "Fail" + reason
                    break
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result
     
    ''' tc6 and tc7 verify that device manager decodes GET
        Send GET with parameter as parameter_a
    '''
    def tc11_get_without_connect(self, dbname):
        
        time.sleep(5)
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            cmd = "GET" + ' ' + self.connect_handle + dbname + "\n"
            self.dm.sendcommand(cmd)
            val = self.dm.recievedata()
            if val.find("ERROR") != -1:
                self.result = "Pass"
            else:
                reason = "GET command failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result 
    
    ''' tc6 and tc7 verify that device manager decodes GET
        Send GET with parameter as parameter_a
    '''
    def tc12_get_with_invalid_conhandler(self, dbname):
        
        invalid_handle="2234"
        time.sleep(5)
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            cmd = "GET" + ' ' + invalid_handle + dbname + "\n"
            self.dm.sendcommand(cmd)
            val = self.dm.recievedata()
            if val.find("ERROR") != -1:
                self.result = "Pass"
            else:
                reason = "GET command failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result 
    
    ''' testcase to send disconnect when connection 
        exists
    '''
    def tc13_disconnect_connection(self):
       
        time.sleep(5)
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            cmd="DISCONNECT " + " " + self.connect_handle+"\n"
            self.dm.sendcommand(cmd)
            time.sleep(1)
            val = self.dm.recievedata()
            if val.find("OK") != -1:
                self.connect_handle = val
                self.result = "Pass"
            else:
                reason = "Disconnect failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result
    
    ''' testcase to send Disconnect with invalid handler
    '''
    def tc14_disconnect_invalid_connection(self):

        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            self.connect_handle="1234"
            cmd="DISCONNECT " + " " + self.connect_handle+"\n"
            self.dm.sendcommand(cmd)
            time.sleep(1)
            val = self.dm.recievedata()
            if val.find("ERROR") != -1:
                self.connect_handle = val
                self.result = "Pass"
            else:
                reason = "Disconnect failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result
    ''' testcase send DISCONNECT when no connection exists
    '''   
    def tc15_disconnect_no_connection(self):
        self.connect_handle="1234"
        if self.setup_connect:
            cmd="DISCONNECT " + " " + self.connect_handle+"\n"
            self.dm.sendcommand(cmd)
            time.sleep(1)
            val = self.dm.recievedata()
            if val.find("ERROR") != -1:
                self.connect_handle = val
                self.result = "Pass"
            else:
                reason = "Disconnect failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result
    '''Testcase for disconnect with connect handler
       value in decimal
    '''
    def tc16_disconnect_connection_integer(self):
        
        time.sleep(5)
        #convert value to integer
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            connect_handle_int=int(self.connect_handle,0)
            cmd="DISCONNECT" + " " + str(connect_handle_int) +"\n"
            self.dm.sendcommand(cmd)
            time.sleep(1)
            val = self.dm.recievedata()
            if val.find("OK") != -1:
                self.result = "Pass"
            else:
                reason = "Disconnect failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result  
    
    def tc17_reset_connection(self):
        
        time.sleep(5)
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            cmd = "RESET" + "\n"
            self.dm.sendcommand(cmd)
            time.sleep(1)
            self.result = "Pass"
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result  
    
    
    def tc18_reset_during_get(self):
        
        time.sleep(5)
        if self.setup_connect:
            self.testcase_sendreset()
            self.tc1_dminitialize()
            self.tc2_establishConnection()
            cmd = "GET" + ' ' + self.connect_handle + " parameter_a" + "\n"
            self.dm.sendcommand(cmd)
            self.testcase_sendreset()
            val = self.dm.recievedata()
            if val.find("0x1ff03") ==0:
                self.connect_handle = val
                self.result = "Pass"
            else:
                reason = "GET command failed"
                self.result = "Fail" + reason
        else:
            reason = " Connection to server failed"
            self.result = "Fail" + reason
        return self.result 
    
    ''' function for executing all testcases
        results are updated in dictionary
    '''
    def executetestcase(self):
        self.device_setup()
        print "Starting TestCase 1"
        self.tcresults['TestCase1']= self.tc1_dminitialize()
        print "Starting TestCase 2"
        self.tcresults['TestCase2']= self.tc2_establishConnection()
        print "Starting TestCase 3" 
        self.tcresults['TestCase3']= self.tc3_establishConn_invalid_addr()
        print "Starting TestCase 4" 
        self.tcresults['TestCase4']= self.tc4_establish_connection_addr_integer()
        print "Starting TestCase 5"
        self.tcresults['TestCase5']= self.tc5_establish_connection_exists_devmanager()
        print "Starting TestCase 6"
        self.tcresults['TestCase6']= self.tc6_tc7_get_database_para1(' parameter_a')
        print "Starting TestCase 7"
        self.tcresults['TestCase7']= self.tc6_tc7_get_database_para1(' parameter_b')
        print "Starting TestCase 8"
        self.tcresults['TestCase8']= self.tc8_get_database_para1_para2()
        print "Starting TestCase 9"
        self.tcresults['TestCase9']= self.tc9_get_database_invalid_para1()
        print "Starting TestCase 10"
        self.tcresults['TestCase10']= self.tc10_multiple_Get_Request()
        print "Starting TestCase 11"
        self.tcresults['TestCase11']= self.tc11_get_without_connect(' parameter_a')
        print "Starting TestCase 12"
        self.tcresults['TestCase12']= self.tc12_get_with_invalid_conhandler(' parameter_a')
        print "Starting TestCase 13"
        self.tcresults['TestCase13']= self.tc13_disconnect_connection()
        print "Starting TestCase 14"
        self.tcresults['TestCase14']= self.tc14_disconnect_invalid_connection()
        print "Starting TestCase 15"
        self.tcresults['TestCase15']= self.tc15_disconnect_no_connection()
        print "Starting TestCase 16"
        self.tcresults['TestCase16']= self.tc16_disconnect_connection_integer()
        print "Starting TestCase 17"
        self.tcresults['TestCase17']= self.tc17_reset_connection()
        print "Starting TestCase 18"
        self.tcresults['TestCase18']= self.tc18_reset_during_get()
        print "Results", self.tcresults
        self.quit()
        self.updateresults()
    
    # member function for Tkinter initialisation
    
    def gui(self):
        
        self.root.title("Device Manager Automation")
        self.root.geometry("400x300")
        app = Frame(self.root)
        app.grid()
        button1 = Button(app, text=" Click to Start Automation", command=lambda: self.executetestcase())
        button1.grid()
        button1.pack(side = 'bottom', padx = 35, pady = 35)
        w = Label(app, text="Start Automation")
        w.pack()
        w1=Label(app,text="Once execution completed results will be opened in default browser")
        w1.pack()
        self.root.mainloop()
    
    #close the window when done
    
    def quit(self):
        self.root.destroy()  
    
    ''' update results in html
        results stored in Result.html
        opens automatically with default browser
    '''      
    def updateresults(self):
        
    
        htmlfile = open("Result.html", "w")
        htmlfile.write("<html><head></head>")
        htmlfile.write("<body><p> Device Manager :  Automation Results</p> </body>")
        htmlfile.write('<table border=1>')
        htmlfile.write("<tr><th>TestCase</th><th>Result</th></tr>")
        htmlfile.write('<tr>')

        for keys in self.tcresults:
                
                htmlfile.write('<th>' + keys + '&nbsp''&nbsp''&nbsp''&nbsp' '</th>')
                htmlfile.write('<th>' + self.tcresults[keys] + '&nbsp''&nbsp''&nbsp''&nbsp' '</th>')
                htmlfile.write('</tr>')
        htmlfile.write('</tr>')
        htmlfile.write('</table>')
        htmlfile.write('</html>')
                                
        htmlfile.close()
        
        webbrowser.open_new_tab('Result.html')
        
if __name__ == "__main__":
    
    test = testsuitedm()
    test.gui()
    raw_input("Done,Press any key to close")
    
    
