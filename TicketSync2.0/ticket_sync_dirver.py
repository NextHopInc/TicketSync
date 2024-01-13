"""
This is the class that everything passes through, this is the driver class

"""
#importing the files (CREATED BY ME Riley Hall @Copyright NextHop Solutions inc)
from new_syncro_alert import Collect_Syncro_Alert as csa
import connectwise_ticket_collection as connectwise
from connectwise_ticket import ticket_object as tik
from error_handler import error_code_handler

#importing the exterior libraries
import json
import datetime as date
import time
import os
#Checks for enabled alerts (ENABLE THEM IN THE SETTINGS.JSON FILE) switch the "false" to true os.path.dirname(os.path.abspath(__file__))+ 
def check_enabled_alerts(): 
    settings = "settings.json"
    print(settings)
    enabled_tiggers = []
    temp_dict = {}
    with open(settings , "r")as read: 
        js = json.load(read)
    for alert in js.get("settings").get("Alerts"): 
        try:
            temp_dict = js.get("settings").get('Alerts').get(alert)
            print("\n\n",temp_dict )
            
            if(temp_dict.get("enabled")=="true"): 
                
                enabled_tiggers.append(temp_dict.get("trigger"))
        except Exception as e: 
            temp_dict = js.get("settings").get('Alerts')
            print("LIST\n\n" , temp_dict)
            print("\n\n" , e)
            
    print(enabled_tiggers)
    return enabled_tiggers
#Sends request to new_syncro_alert to get all the alerts with the possible trigger that is passed into it
def get_syncro_alerts(trigger): 
    sa = csa(trigger)
    data = sa.request_data()
    print("HELLO")
    #alert_list contains all alerts with the right check type
    alert_list = sa.clean_data(data)
    return alert_list
#Sends request to connectwuse_ticket_collection to find the correct configuration. We use the company ID because it is unique and is easily identifiable 
def find_configuration(computer_name , company_id, id,  cw): 
    #Make call to connectwise_ticket_collection 
    configuration_status = cw.collect_configuration_data(computer_name,company_id,id)
    return configuration_status
#This is the main loop. Once the timer is done in main we iterate through this loop and this function also calls all the other functions
def ticket_creation_loop(enabled_triggers): 
    for trigger in enabled_triggers:
        alert_list = get_syncro_alerts(trigger=trigger)
        #For ever enabled trigger in the settings.json file we iterate once through the following loop
        for alert in alert_list: 
            #For every alert scraped from Syncro MSP rmm_alerts we iterate through it trying to find if it has a ticket yet or not 
            cw = connectwise.ConnectWise_Ticket_Collection(computer_name=alert[0] , company_name=alert[1] , unique=alert[2],trigger=trigger)
            #This checks if there is a ticket for the alert yet. If there is then it returns the ticketnumber and true also we pull company id 
            is_real = cw.check_is_real()
            print(is_real)
            alert_id = alert[2]
            #If Ticket has been created and we need to patch new notes to it
            
            if(is_real[0]): 
                #Create patch statement
                tk = tik(ticket_data={})

                patch = tk.patch_request(alert[3],is_real[1])
                cw.patch_request(patch=patch,ticket_number=is_real[1])
                configuration_status = find_configuration(alert[0],is_real[2],is_real[1] ,cw=cw)
                #Check if ticket has configuration.. If not then add. Else do nothing 
                # print(configuration_status , configuration_status.json())
                print(error_code_handler(configuration_status))

            #If ticket needs to be created 
            else: 
                # Here we are collecting the needed information to form the tickets. Company name , company id , site id etc 
                ticket_data = cw.collect_ticket_data()
                #This is to create a ticket object. We pass in the data that we already gathered in the previous call (ticket_data = cw.collect_ticket_data())
                tk = tik(ticket_data=ticket_data)
                ticket = tk.new_ticket()
                
                #Now we post the ticket
                ticket_number = cw.post_request(ticket)
                elpatch = tk.patch_request(alert[3], ticket_number)
                #Patch the notes
                cw.patch_request(elpatch , ticket_number=ticket_number)
                #Adds the configurations to the ticket
                status =find_configuration(alert[0],ticket_data.get("company_id") ,ticket_number , cw=cw)
                print(status , status.json())

            #Now we have to mute and delete the alert from SyncroMSP. This doesn't need to be done in a condition since it needs to be done regardless of it it was a new ticket or not
            mute_status = csa.mute_alert(alert_id)
            delete_status = csa.delete_alert(alert_id)
            
            print(f"MUTE {error_code_handler(mute_status)} and DELETE {error_code_handler(delete_status)}")
            #Remove this....
            
    return
        

def main(): 
    #Need countdown timer os.path.dirname(os.path.abspath(__file__))+
    settings =  "settings.json"
    print(settings)
    enabled_triggers = check_enabled_alerts()
    ticket_creation_loop(enabled_triggers=enabled_triggers)
    try:
        with open(settings , "r") as read: 
            data = json.load(read)
           
        flag = True
        countDownTime = data.get("settings").get("timer")
        countDownTime = int(countDownTime)
    except: 
        countDownTime = 13
        flag = True
        #iterate through this while loop until flag is false then we can start the program. It is set to run at 11am but if the file cannot be found we run at default time of 10pm
    while(flag):

        local = date.datetime.now()
        if(local.second == 0 and local.minute == 0):
            if(countDownTime == local.hour): 
                print("Starting program")
                flag = False
            

        current_time = time.strftime("%H:%M:%S" , time.localtime())
        
        print( current_time , end='\r')
        time.sleep(1)
    main()
    
        #Once countdown timer is done we run the program
   
        #Triggers go here 
if __name__=='__main__': 
    main()
