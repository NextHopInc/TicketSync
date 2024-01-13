import os
import datetime

class error_code_handler: 
    def __init__(self,error_code):
        self.error_code = error_code

    def handler(self): 

        if(self.error_code==201): 
            return "Created"
        elif(self.error_code==200):
            return "Complete"
        elif(self.error_code==204): 
            return "no content"
        elif(self.error_code==400): 
            return "Bad Request"
        elif(self.error_code==401): 
            return "Unauthorized"
        elif(self.error_code==403): 
            return "Forbidden"
        elif(self.error_code==404): 
            return "Not Found"
        elif(self.error_code==405): 
            return "Method Not Allowed"
        elif(self.error_code==409): 
            return "Conflict"
        elif(self.error_code==415): 
            return "Unsupported Media Type"
        elif(self.error_code==500): 
            return "Server Error"
        else: 
            return (self.error_code, "Unforeseen Error")
         
class crash_handler: 
    def __init__(self,error):
        self.error = error

    def handler(self): 
        crash_report = os.path.dirname(os.path.abspath(__file__))+"\\crash_report.txt"
        with open(crash_report , "w")as write:
            write.write(datetime.datetime.now()) 
            write.write(self.error)
            write.flush() 
            write.close()
        
