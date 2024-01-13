import json
import os
class ticket_object: 
    def __init__(self , ticket_data):
        self.ticket_data = ticket_data

    def  new_ticket(self):
        settings = "settings.json"
        keys = None 
        key = ""
        with open(settings, "r")as read:
            js = json.load(read)
            keys = js.get("settings").get("Alerts").get(self.ticket_data.get("trigger")).get("key_words")
            read.close()
        for i in keys:
            key+= " "+ i
        print(self.ticket_data , key)
        json1 ={
        "id": 0,
        "summary": "Computer " + self.ticket_data.get("name") + " " + self.ticket_data.get("trigger") +  key,
        "recordType": "ServiceTicket",
        "board": {
            "id": 26,
            "name": "Alerts",

        },
        "status": {
            "id": 351,
            "name": "New",

        },
        "workRole": {
            "id": 22,
            "name": "Help Desk Engineer",
    
        },
        "workType": {
            "id": 18,
            "name": "Remote Support",

        },
        "company": {
            "id": self.ticket_data.get("company_id"),
            "identifier": self.ticket_data.get("company_name"),
            "name": self.ticket_data.get("company_name"),

        },
        "site": {
            "id": self.ticket_data.get("site_id"),
            "name": "main",
        },
        "contact": {
            "id": self.ticket_data.get("contact_id"),
            "name": self.ticket_data.get("contact_name"),
        },
        "contactName": self.ticket_data.get("contact_name"),
        "team": {
            "id": 55,
            "name": "Alerts",
        },

        "priority": {
            "id": 3,
            "name": "Priority 4 - Scheduled Maintenance",
            "sort": 8,

        },
        "serviceLocation": {
            "id": 1,
            "name": "On-Site",

        },
        "source": {
            "id": 1,
            "name": "Email",

        },
        "severity": "Medium",
        "impact": "Medium",
        "allowAllClientsPortalView": False,
        "customerUpdatedFlag": False,
        "automaticEmailContactFlag": True,
        "automaticEmailResourceFlag": True,
        "automaticEmailCcFlag": True,
        "processNotifications": True,
        "skipCallback": True,
        "closedFlag": True,
        "actualHours": 0,
        "approved": True,
        "estimatedExpenseCost": 0.00,
        "estimatedExpenseRevenue": 0.00,
        "estimatedProductCost": 0.00,
        "estimatedProductRevenue": 0.00,
        "estimatedTimeCost": 0.00,
        "estimatedTimeRevenue": 0.00,
        "billingMethod": "ActualRates",
        "subBillingMethod": "ActualRates",
        "isInSla": False,
        "hasChildTicket": False,
        "hasMergedChildTicketFlag": False,
        "knowledgeBaseLinkType": "Activity",
        "billTime": "NoDefault",
        "billExpenses": "NoDefault",
        "billProducts": "NoDefault",
        "predecessorType": "Ticket",
        "location": {
            "id": 2,
            "name": "Abbotsford",

        },
        "department": {
            "id": 16,
            "identifier": "Operations",
            "name": "Operations",

        },
        "mobileGuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "sla": {
            "id": 5,
            "name": "No Contract",

        },
        "slaStatus": "string",
        "currency": {
            "id": 1,
            "symbol": "C$",
            "currencyCode": "CAD",
            "decimalSeparator": ".",
            "numberOfDecimals": 2,
            "thousandsSeparator": ",",
            "negativeParenthesesFlag": False,
            "displaySymbolFlag": False,
            "currencyIdentifier": "CDN",
            "displayIdFlag": False,
            "rightAlign": False,
            "name": "Canadian Dollars",

        },

    }
        return json1

    def patch_request(self , new_value , ticket_id): 
        #Adding notes to the ticket 
        patch = {
            "id" : 0,
            "ticketId" : ticket_id, 
            "text" : new_value,
            "detailDescriptionFlag": 1,
            "internalAnalysisFlag": 0,
            "resolutionFlag": 0,
            "issueFlag": 0, 
        }
        return patch
   
        
        
