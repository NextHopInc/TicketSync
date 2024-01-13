"""
This class gathers Tickt Data from ConnectWise. Checks to see if ticket exists or not. 
Returns true if ticket exists and false if it doesn't 
"""
import os
import requests as req
import secret_key as keys
import json
class ConnectWise_Ticket_Collection: 


    def __init__(self , company_name , computer_name , unique , trigger):
        
        cwToken = keys.generateToken()
        #Getting CodeBase might change upon update (ConnectWise End)
        code_data = req.get("https://na.myconnectwise.net/login/companyinfo/connectwise")
        codebase = code_data.json().get("Codebase")

        self.cwURL = "https://api-na.myconnectwise.net/"+codebase+"//apis/3.0/"
        self.cwheaders = {"Authorization" : "Basic " + cwToken, "clientID": keys.getCW_ClientID() , "Content-Type":"application/json; charset=utf-8"  , "Accept" : "application/vnd.connectwise.com+json; version=2022.1"
    }
        self.company_name = company_name
        self.computer_name = computer_name
        #unique identifier that we add to tickets to make it easily searchable 
        self.unique = unique
        self.trigger = trigger
        print("TICKET OBJECT CREATION \n" , self.company_name , self.trigger)
        

    #This is the function that we try to find if the ticket exists 
    def check_is_real(self):
        settings = "settings.json"
        print(self.company_name , " " , self.computer_name)
        #Company Names - They can have a & and or other special characters. We need to clean those signs and replace them with the correct characters like %20 for spaces
        if ("&" in self.company_name): 
            self.company_name = self.company_name.replace("&" , "%26")
        if(self.company_name =="Oval Village Law" ): 
            self.company_name += " Corporation"
        if("+" in self.company_name): 
            self.company_name = self.company_name.replace("+","%2b")
        data = req.get(url=self.cwURL+f'/service/tickets?fields=id,summary,company/name,company/id&conditions=board/name="Alerts" AND company/name="{self.company_name}" AND summary contains "{self.computer_name}" AND status/name!="Completed" AND status/name!="Closed"',headers=self.cwheaders)

        #This is to find if tickets exist 
        #We do this by getting all tickets from alert board and from specified company and also need to have computer name in summary, then from there we look at the status 
        #After that we are returned x amount of tickets and then we iterate through them seeing if any contain the key words 

        with open(settings , "r") as read: 
            js = json.load(read)
            key_words = js.get("settings").get("Alerts").get(self.trigger).get("key_words")
            read.close()
        access = 0
        print(data.json())



        if(len(data.json())>0):
            for ticket in data.json(): 
                access = 0
                for key in key_words: 
                    print("TICKET   " , ticket)
                    # print( f"key={key} ", ticket.get("summary").lower().replace("_"," "))
                    if(key.lower() in ticket.get("summary").lower().replace("_"," ")): 
                        access+=1
                if(access == len(key_words)): 
                    return (True , ticket.get("id") , ticket.get("company").get("id") ) 
    
        else: 
            return (False, "")
        return (False,"")
    
            

    def collect_ticket_data(self): 
        #This method will get company Id , Site Id , contact ID and also contact name
        print(self.company_name)
        if ("&" in self.company_name): 
            self.company_name = self.company_name.replace("&" , "%26")
        if(self.company_name =="Oval Village Law" ): 
            self.company_name += " Corporation"
        if("+" in self.company_name): 
            self.company_name = self.company_name.replace("+","%2b")
    
        data = req.get(url=f"https://api-na.myconnectwise.net/v2022_2////apis/3.0/company/companies?fields=site,id,name,defaultContact&conditions=name='{self.company_name}'" , headers=self.cwheaders)
        xdata = data.json()[0]
       
        company_id = xdata.get("id")

        contact_id = xdata.get("defaultContact").get("id")
        contact_name = xdata.get("defaultContact").get("name")
        site_id = xdata.get("site").get("id")
        site_name = xdata.get("site").get("name")

        return {"company_id" : company_id , "contact_id" : contact_id , "contact_name" : contact_name , "site_id" : site_id , "site_name" : site_name , "trigger" : self.trigger , "name" : self.computer_name}
    
    def collect_configuration_data(self,config_name,company_id , id): 
        configs = req.get(url=self.cwURL+f"/company/configurations?fields=id,name&conditions=company/id={company_id} AND name='{config_name}'", headers=self.cwheaders)
        
        if(len(configs.json())>0):
            print("CONFIGURATIONS " ,configs.json() , "Computer Name " , config_name)
            config_request = { 
                "id" : configs.json()[0].get("id"),
                "deviceIdentifier" : configs.json()[0].get("name")
            }
        else: 
            return 405
 
        status = req.post(url=self.cwURL+f"/service/tickets/{id}/configurations",json=config_request,headers=self.cwheaders)
        return status

    #These add the tickts and update them these are the functions that actually send the posts requests
    def patch_request(self,patch, ticket_number): 
        status = req.post(url=self.cwURL+f"/service/tickets/{ticket_number}/notes",json=patch,headers=self.cwheaders)
        
        return status
    
    def post_request(self,post): 
        status = req.post(url=self.cwURL+f"/service/tickets",json=post,headers=self.cwheaders)
        print(status.status_code)

        ticket_number = status.json().get("id")
        return ticket_number
    
    
        
