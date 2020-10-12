#BIOS parameters management
## Description
The workflow is example how BIOS parameters management could be automated via MSA. The workflow is able to work in two modes:
 - **New server provisioning **. This mode is proposed to work with new server. This mode performs:
    - Identifies server vendor based on OUI in provided MAC address using [this server description file](https://github.com/openmsa/Workflows/blob/master/BIOS_Automation/BIOS_parameters_management/server_profiles.json);
    - Creates new MSA managed entity (ME) and activates it;
    - Changes BIOS parameters regarding attached profile. Profiles defenitions are in [this server description file](https://github.com/openmsa/Workflows/blob/master/BIOS_Automation/BIOS_parameters_management/server_profiles.json);
    - Changes default BMC password.
 The workflow requires the following parameters as input:
    - BIOS profile. Profiles are defined for each vendor in [this server description file](https://github.com/openmsa/Workflows/blob/master/BIOS_Automation/BIOS_parameters_management/server_profiles.json);
    - Server IP address;
    - Server MAC address. It used to identify server vendor;
 - **Working with existed server **. This mode is proposed to work already provisioned server. This mode performs:
    - Changes BIOS parameters regarding attached profile. Profiles defenitions are in [this server description file](https://github.com/openmsa/Workflows/blob/master/BIOS_Automation/BIOS_parameters_management/server_profiles.json);
    
## Prerequisites
The current implementation works with server Intel and Dell which support Redfish API. To adopt new server, the following actions are required:
 - Adopte [the microservices](https://github.com/openmsa/Microservices/tree/master/REDFISHAPI/Generic) for new vendor;
 - Add new vendor defenition to [this server description file](https://github.com/openmsa/Workflows/blob/master/BIOS_Automation/BIOS_parameters_management/server_profiles.json);
 - If the vendor Redfish implementation supports job management, add the attribute using this JSON section:
 '''
                 "Miscellaneous parameters": {
                        "JobManager": true
                }
'''
