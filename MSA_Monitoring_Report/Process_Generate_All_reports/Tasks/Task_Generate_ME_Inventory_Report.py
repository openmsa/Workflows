from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.lookup import Lookup
from msa_sdk import constants
from datetime import date
import requests
import json
import urllib3
import csv

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    msa_var = Variables()
    context = Variables.task_call(msa_var)
    
    msa_ip    = context["msa_ip"]
    
    # Get tenant details
    tenant_details = {}
    _url = 'https://' + msa_ip + '/ubi-api-rest/lookup/v1/operators'
    token = context["msa_token"]
    _headers={'Content-Type':'application/json', 'Accept': 'application/json',
              'Authorization': 'Bearer ' + token
    }
    _payload= {}
    response = requests.get(url=_url, headers=_headers, verify=False, timeout=120)
    tenants = response.json()
    for tenant in tenants:
        tenant_prefix = tenant["prefix"]
        tenant_details[tenant_prefix] = tenant["name"]
        
    # Get subtenant details
    subtenant_details = {}
    _url = 'https://' + msa_ip + '/ubi-api-rest/lookup/customers'
    token = context["msa_token"]
    _headers={'Content-Type':'application/json', 'Accept': 'application/json',
              'Authorization': 'Bearer ' + token
    }
    _payload= {}
    response = requests.get(url=_url, headers=_headers, verify=False, timeout=120)
    subtenants = response.json()
    for subtenant in subtenants:
        subtenant_id = subtenant["id"]
        subtenant_details[subtenant_id] = subtenant["name"]
    
    # Get manufacturer and model details
    manufacturer_details = {}
    model_details = {}
    _url = 'https://' + msa_ip + '/ubi-api-rest/device/v1/manufacturers'
    token = context["msa_token"]
    _headers={'Content-Type':'application/json', 'Accept': 'application/json',
              'Authorization': 'Bearer ' + token
    }
    _payload= {}
    response = requests.get(url=_url, headers=_headers, verify=False, timeout=120)
    output_code = response.status_code
    if int(output_code) < 400:
        manufacturers = response.json()
        for manufacturer in manufacturers:
            manufacturer_id = manufacturer["manufacturerId"]
            manufacturer_details[manufacturer_id] = manufacturer["manufacturerName"]
            models = manufacturer["models"]
            for model in models:
                model_id = model["modelId"]
                model_details[model_id] = model["modelName"]
    else :
        ret = MSA_API.process_content('FAIL', f' Unable to get manufacturer and model details. Error message: {response.json()}', context, True)
    
    
    
    # Get all managed entity details & status
    me_status_details = {"totalME": 0, "OK": 0, "NEVERREACHED": 0, "ERROR": 0}
    me_table = {}
    _url = 'https://' + msa_ip + '/ubi-api-rest/assetManagement/v1/customer-asset/manager/1'
    token = context["msa_token"]
    _headers={'Content-Type':'application/json', 'Accept': 'application/json',
              'Authorization': 'Bearer ' + token
    }
    _payload= {}
    response = requests.get(url=_url, headers=_headers, verify=False, timeout=120)
    output_code = response.status_code
    if int(output_code) < 400:
        me_details = response.json()
        for me_detail in me_details:
            me_status_details["totalME"] += 1 
            me_id = str(me_detail["deviceID"])
            me_table[me_id] = {}
            me_table[me_id]["me_name"] = me_detail["name"]
            prefix = me_detail["prefix"]
            me_table[me_id]["tenant"] = tenant_details[prefix]
            subtenant_id = me_detail["abonneId"]
            me_table[me_id]["subtenant"] = subtenant_details[subtenant_id]
            manId = me_detail["manId"]
            me_table[me_id]["vendor"] = manufacturer_details[manId]
            modId = me_detail["modId"]
            me_table[me_id]["model"] = model_details[modId]
            me_table[me_id]["ip_address"] = me_detail["ipConfig"]
            me_table[me_id]["status"] = me_detail["pingStatus"]
            me_status_details[me_detail["pingStatus"]] += 1
        
        context["me_status_details"] = me_status_details
        # Create csv report file
        report_file_name = "me_details_report_" + str(date.today()) + ".csv"
        report_file_path = "/opt/fmc_repository/Documentation/" + report_file_name
        with open(report_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["Managed Entity Name", "Tenant", "Subtenant", "Vendor", "Model", "IP Address", "Status"]
        
            writer.writerow(field)
            for me in me_table:
                me_detail = me_table[me]
                writer.writerow([me_detail["me_name"], me_detail["tenant"], me_detail["subtenant"], me_detail["vendor"], me_detail["model"], me_detail["ip_address"], me_detail["status"]])

        context["me_details_report"] = report_file_path
        ret = MSA_API.process_content('ENDED', f' Managed Entity Details csv created: {report_file_name}', context, True)
    else :
        ret = MSA_API.process_content('FAIL', f' Unable to get Managed Enity details. Error message: {response.json()}', context, True)
    
    print(ret)