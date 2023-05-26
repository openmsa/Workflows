from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.lookup import Lookup
from msa_sdk import constants
from datetime import date,datetime
import os.path
import requests
import json
import urllib3
import csv

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    msa_var = Variables()
    context = Variables.task_call(msa_var)
    
    msa_ip    = context["msa_ip"]
    me_status_details = context["me_status_details"]
    # Create csv report file
    report_file_name = "me_status_report_" + str(msa_ip) + ".csv"
    report_file_path = "/opt/fmc_repository/Documentation/" + report_file_name
    
    file_exists = os.path.isfile(report_file_path)
    # dd/mm/YY H:M:S
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(report_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        field = ["Time", "Total ME", "UP ME", "NR ME", "Critical ME"]
    
        if not file_exists:
            writer.writerow(field)
        writer.writerow([dt_string, me_status_details["totalME"], me_status_details["OK"], me_status_details["NEVERREACHED"], me_status_details["ERROR"]])
    context["me_status_report"] = report_file_path
    ret = MSA_API.process_content('ENDED', f' Managed Entity Status Details csv created: {report_file_name}', context, True)
    print(ret)