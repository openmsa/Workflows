import copy
import json
import re
import os
import subprocess


from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import xml.etree.ElementTree as ET
import numpy as np
#from re import search
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import requests
from xml.dom import minidom
#from xml.dom.ext.reader.Sax2 import FromXmlStream
from msa_sdk.device import Device

dev_var = Variables()
context = Variables.task_call(dev_var)
yang_fields_without_child = context['yang_fields_without_child_hash'].keys()

msa_object  = MSA_API()
msa_object.action = 'Create MS object'
msa_object.path   = "/repository/v2/resource/microservice"


# Build the curl command to create the Micro Service

ms_name     =  str(os.path.basename(context['main_yang_file']).replace(context['yangs_extension'],''))
ms_filename = "CommandDefinition/microservices/" + ms_name  + '.xml'


curl_ms_creation_xml =  """ {
  "information": {
    "displayName": """+ '"'+  ms_name +  """",
    "icon": "none",
    "description": """ +'"'+  ms_name +  """",
    "category": "Default",
    "displayField": "object_id",
    "order": 0,
    "visibility": "5",
    "configType": "netconf"
  },
  "variables": {
    "variable": [
      {
        "displayName": "object_id",
        "fullDisplayName": "",
        "displayNameHeader": "",
        "displayOrder": 0,
        "name": "params.object_id",
        "description": "",
        "type": "String",
        "visible": true,
        "userLocked": false,
        "onlyDetailView": false,
        "grouped": false,
        "groupDisplayName": "",
        "groupSeparator": "",
        "mandatory": false,
        "editable": false,
        "arrayCanAdd": true,
        "arrayCanRemove": true,
        "arrayCanMove": true,
        "arrayCanEdit": true
      } """

for yang_good_field in yang_fields_without_child:
  curl_ms_creation_xml = curl_ms_creation_xml + """,
      {
        "displayName": """ + '"'+  yang_good_field +  """",
        "fullDisplayName": """ + '"'+  yang_good_field +  """",
        "displayNameHeader": "",
        "displayOrder": 0,
        "name": "params.""" +  yang_good_field +  """",
        "description": "",
        "type": "String",
        "visible": true,
        "userLocked": false,
        "onlyDetailView": false,
        "grouped": false,
        "groupDisplayName": "",
        "groupSeparator": "",
        "mandatory": false,
        "editable": false,
        "arrayCanAdd": true,
        "arrayCanRemove": true,
        "arrayCanMove": true,
        "arrayCanEdit": true
      } """

curl_ms_creation_xml = curl_ms_creation_xml + """
    ],
    "frozen": 0
  },
  "command": [
    {
      "operation": null,
      "name": "IMPORT",
      "postTemplate": null,
      "parser": {
        "section": [
          {
            "xpath": ""
          }
        ],
        "lines": {}
      }
    },
    { 
      "operation": " """
yang_create_operations = ''
#get Create part from xml
f = open(context['xml_create_output_file'], "r")
string_create_part = f.read() 
string_create_part = string_create_part.replace('\"','\\"')  #protect " in the string
string_create_part = string_create_part.replace('\n','\\n')  #protect end of line for json convertion
yang_create_operations = yang_create_operations + string_create_part + '" '

curl_ms_creation_xml = curl_ms_creation_xml + yang_create_operations + """,
      "name": "CREATE"
    },
    {
      "operation": null,
      "name": "READ"
    },
    {
      "operation": " """
curl_ms_creation_xml = curl_ms_creation_xml + yang_create_operations + """,
      "name": "IMPORT"
    },
    {
      "operation": null,
      "name": "UPDATE"
    },
    {
      "operation": null,
      "name": "CONSTRAINT"
    },
    {
      "operation": null,
      "name": "DELETE"
    },
    {
      "operation": null,
      "name": "LIST"
    }
  ],
  "example": {
    "content": " """
curl_ms_creation_xml = curl_ms_creation_xml + yang_create_operations + """
  },
  "metaInformationList": [
    {
      "type": "FILE",
      "uri": """+ '"'+  ms_filename +  """",
      "file": true,
      "name": """+  '"'+ ms_name + '.xml' + """",
      "displayName": """+ '"'+  ms_name + '.xml' + """",
      "repositoryName": "CommandDefinition",
      "parentURI": "CommandDefinition",
      "fileType": "text",
      "tag": "string",
      "comment": "string",
      "modelId": 137,
      "vendorId": 1
    }
  ]
}  
"""


context.update(curl_ms_creation_xml=curl_ms_creation_xml)

#Uncomment following lines to degub, check the contain of following file, it should be convertible into one json array (it it is the curl request parameter)
#fw = open(context['xml_create_output_file']+'_curl_content.json', "w")
#fw.write(curl_ms_creation_xml)
#fw.close()
 

parameters_json = json.loads(curl_ms_creation_xml)
#Create the MicroService with Culr requests
msa_object.call_post(parameters_json)


context['micro_service_file'] = ms_filename

ret = MSA_API.process_content(constants.ENDED, ' New MicroService "'+ ms_name + '" created', context, True)
print(ret)


