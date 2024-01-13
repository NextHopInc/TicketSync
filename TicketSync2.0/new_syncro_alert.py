"""
This class will deal with gathering the data from SyncroMSP. We will do this through the SyncroMSP Rest API.
1) We will request all new alerts with the specified alert
2) then send to our ticket creating object

"""

import requests as req
import ssl
class Collect_Syncro_Alert:
    def __init__(self , check_type):
        #Pass in the alert we are looking for. 333998974
        self.check_type = check_type
        self.syncro_url = "https://nexthop.syncromsp.com/api/v1/"
        self.api_key = "?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328"
    def request_data(self): 
        pages = req.get(url="https://nexthop.syncromsp.com/api/v1/rmm_alerts?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328" , verify=ssl.CERT_NONE)
        pages = pages.json().get("meta").get("total_pages")
        
        data = req.get(url=f"https://nexthop.syncromsp.com/api/v1/rmm_alerts?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328" , verify=ssl.CERT_NONE)
        
        return data.json()
    
    def clean_data(self , data):
       
        alert_list = []
        for i in range(len(data.get("rmm_alerts"))): 
            if(self.check_type in data.get("rmm_alerts")[i].get("properties").get("trigger")): 
                #If we find one and enter this clause we have a hit. Now we need to create a ticket object for it. Or we have to check if a ticket was already created for it... 
                hit = data.get("rmm_alerts")[i]
                #Get ConnectWise filter through REST API to check if ticket is already created 
                customer_data = req.get(url=self.syncro_url+"customers/"+str(hit.get("customer_id"))+self.api_key)
                business_name = customer_data.json().get("customer").get("business_name")
                alert_number = hit.get("id")
                #Grab computer name so we can find all tickets that have this computer name and this company name 
                computer_name = hit.get("computer_name")
                description = hit.get("properties").get("description")
                print("hit")
                alert_list.append((computer_name , business_name , alert_number , description))


        if(len(alert_list)<=0): 
            print("No alerts " , alert_list)
            
        else: 
            print(alert_list)
            
            return alert_list
    @classmethod
    def mute_alert(self,alert_id): 
        status = req.post(f"https://nexthop.syncromsp.com/api/v1/rmm_alerts/{alert_id}/mute?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&mute_for=1-week")
        return status
    
    @classmethod
    def delete_alert(self,alert_id): 
        status = req.delete(f"https://nexthop.syncromsp.com/api/v1/rmm_alerts/{alert_id}?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328")
        print(status.status_code , "   " , status.json())
        return status

