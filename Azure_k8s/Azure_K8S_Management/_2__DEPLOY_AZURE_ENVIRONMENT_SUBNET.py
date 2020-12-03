import json
import time
import requests
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])


class AZConnection():

    def __init__(self, client_id, client_secret, subscription_id,
                 tenant_id, resource_group, location):
        self.client_id = client_id
        self.client_secret = client_secret
        self.subscription_id = subscription_id
        self.tenant_id = tenant_id
        self.resource_group = resource_group
        self.location = location
        self.token = self.get_token(tenant_id)
        self.base_url = "https://management.azure.com"
        self.net_base_url = "https://management.azure.com" + \
                            "/subscriptions/" + self.subscription_id + \
                            "/resourcegroups/" + self.resource_group + \
                            "/providers/Microsoft.Network"
        self.compute_base_url = "https://management.azure.com" + \
                                "/subscriptions/" + self.subscription_id + \
                                "/resourcegroups/" + self.resource_group + \
                                "/providers/Microsoft.Compute"

    def get_token(self, tenant_id,
                  az_resource="https%3A//management.azure.com"):
        url = "https://login.microsoftonline.com/" + \
              tenant_id + \
              "/oauth2/token"

        payload = 'grant_type=client_credentials' + '&' + \
                  'client_id=' + self.client_id + '&' + \
                  'client_secret=' + self.client_secret + '&' + \
                  'resource=' + az_resource

        headers = {'Content-Type': 'application/x-www-form-urlencoded'
                   }

        response = requests.request("POST", url, headers=headers,
                                      data=payload, verify=True)

        if ('access_token' in response.json().keys()):
            return response.json()['access_token']
        else:
            print(f'ERROR: TOKEN NOT FOUND {response.json()}')
            exit()

    #######################################
    #         /Microsoft.Network          #
    #######################################

    # https://docs.microsoft.com/en-us/rest/api/virtualnetwork/networksecuritygroups/createorupdate
    # creates empty policy
    def sec_group_create(self, sec_gr_name):
        url = self.net_base_url + \
              "/networkSecurityGroups/" + str(sec_gr_name) + \
              "?api-version=2020-05-01"

        payload = {'location': self.location}

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("PUT", url, headers=headers,
                                    data=json.dumps(payload), verify=True)

        return response.json()

    # allows connections from ip address (INBOUND!)
    def sec_group_permit(self, priority, sec_gr_name,
                         rule_name, ip_addr, proto, port):
        url = self.net_base_url + \
              "/networkSecurityGroups/" + str(sec_gr_name) + \
              "?api-version=2020-05-01"

        if proto == 'ICMP':
            port = "*"

        payload = {
                  "properties": {
                    "securityRules": [
                      {
                        "name": rule_name,
                        "properties": {
                          "protocol": proto,
                          "sourceAddressPrefix": ip_addr,
                          "destinationAddressPrefix": "*",
                          "access": "Allow",
                          "destinationPortRange": port,
                          "sourcePortRange": "*",
                          "priority": priority,
                          "direction": "Inbound"
                        }
                      },
                      # STUB for ICMP
                      {
                        "name": "ICMP",
                        "properties": {
                          "protocol": "icmp",
                          "sourceAddressPrefix": ip_addr,
                          "destinationAddressPrefix": "*",
                          "access": "Allow",
                          "destinationPortRange": "*",
                          "sourcePortRange": "*",
                          "priority": str(int(priority) + 10),
                          "direction": "Inbound"
                        }
                      },
                      # STUB for TCP/6443
                      {
                        "name": "tcp_6443",
                        "properties": {
                          "protocol": "TCP",
                          "sourceAddressPrefix": ip_addr,
                          "destinationAddressPrefix": "*",
                          "access": "Allow",
                          "destinationPortRange": "6443",
                          "sourcePortRange": "*",
                          "priority": str(int(priority) + 20),
                          "direction": "Inbound"
                        }
                      }
                    ]
                  },
                  "location": self.location
                }

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("PUT", url, headers=headers,
                                    data=json.dumps(payload), verify=True)

        return response.json()

    # https://docs.microsoft.com/en-us/rest/api/virtualnetwork/virtualnetworks/createorupdate
    # ip_prefix example = "10.0.0.0/16"
    def virt_net_create(self, virt_net_name, ip_prefix):
        url = self.net_base_url + \
              "/virtualNetworks/" + str(virt_net_name) + \
              "?api-version=2020-05-01"

        payload = {
                  "properties": {
                    "addressSpace": {
                      "addressPrefixes": [
                        ip_prefix
                      ]
                    }
                  },
                  "location": self.location
                }

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("PUT", url, headers=headers,
                                    data=json.dumps(payload), verify=True)

        return response.json()

    # https://docs.microsoft.com/en-us/rest/api/virtualnetwork/subnets/createorupdate
    def subnet_create(self, virt_net_name, subnet_name, ip_prefix):
        url = self.net_base_url + \
              "/virtualNetworks/" + str(virt_net_name) + \
              "/subnets/" + str(subnet_name) + \
              "?api-version=2020-05-01"

        payload = {
                  "properties": {
                    "addressPrefix": ip_prefix
                  }
                }

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("PUT", url, headers=headers,
                                    data=json.dumps(payload), verify=True)

        return response.json()

    # https://docs.microsoft.com/en-us/rest/api/virtualnetwork/publicipaddresses/createorupdate
    # name example k8s-node-01-ip
    def public_ip_create(self, public_ip_name, vm_label):
        url = self.net_base_url + \
              "/publicIPAddresses/" + str(public_ip_name) + \
              "?api-version=2020-05-01"

        payload = {
                  "name": str(public_ip_name),
                  "properties": {
                    "publicIPAllocationMethod": "Dynamic",
                    "idleTimeoutInMinutes": 4,
                    "publicIPAddressVersion": "IPv4",
                    "dnsSettings": {
                      "domainNameLabel": vm_label
                    }
                  },
                  "location": self.location
                }

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("PUT", url, headers=headers,
                                    data=json.dumps(payload), verify=True)

        return response.json()

    # https://docs.microsoft.com/en-us/rest/api/virtualnetwork/networkinterfaces/createorupdate
    def nic_create(self, net_iface_name, public_ip_id, subnet_id, sec_group_id):
        url = self.net_base_url + \
              "/networkInterfaces/" + str(net_iface_name) + \
              "?api-version=2020-05-01"

        payload = {
                  "properties": {
                    "enableAcceleratedNetworking": False,
                    "networkSecurityGroup": {
                      "id": sec_group_id
                    },
                    "ipConfigurations": [
                      {
                        "name": net_iface_name,
                        "properties": {
                          "publicIPAddress": {
                            "id": public_ip_id
                          },
                          "subnet": {
                            "id": subnet_id
                          }
                        }
                      }
                    ]
                  },
                  "location": self.location
                }

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("PUT", url, headers=headers,
                                    data=json.dumps(payload), verify=True)

        return response.json()

    #######################################
    #         /Microsoft.Compute          #
    #######################################

    # https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/createorupdate
    # vmSize = Standard_D2s_v3
    # sku = 18.04-LTS
    # offer = UbuntuServer
    # publisher = Canonical
    # version = latest
    def vm_create(self, vm_name, vmSize, sku, offer, publisher, version,
                  username, password, nic_id):
        url = self.compute_base_url + \
              "/virtualMachines/" + str(vm_name) + \
              "?api-version=2020-06-01"

        payload = {
                  "location": self.location,
                  "properties": {
                    "hardwareProfile": {
                      "vmSize": vmSize
                    },
                    "storageProfile": {
                      "imageReference": {
                        "sku": sku,
                        "publisher": publisher,
                        "version": version,
                        "offer": offer
                      },
                      "osDisk": {
                        "caching": "ReadWrite",
                        "managedDisk": {
                          "storageAccountType": "Standard_LRS"
                        },
                        "name": str(vm_name) + '-disk',
                        "createOption": "FromImage"
                      }
                    },
                    "osProfile": {
                      "adminUsername": str(username),
                      "computerName": str(vm_name),
                      "adminPassword": str(password)
                    },
                    "networkProfile": {
                      "networkInterfaces": [
                        {
                          "id": nic_id,
                          "properties": {
                            "primary": True
                          }
                        }
                      ]
                    }
                  }
                }

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("PUT", url, headers=headers,
                                    data=json.dumps(payload), verify=True)

        return response.json()

    def get_vm_status(self, vm_name):
        url = self.compute_base_url + \
              "/virtualMachines/" + str(vm_name) + \
              "?api-version=2020-06-01"

        payload = {}

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("GET", url, headers=headers,
                                    data=payload, verify=True)

        return response.json()

    def get_resource_status(self, rs_id, api_ver):
        url = self.base_url + rs_id + "?api-version=" + api_ver

        payload = {}

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("GET", url, headers=headers,
                                    data=payload, verify=True)

        return response.json()['properties']['provisioningState']

    def get_status_loop(self, rs_id, api_ver, stop=120):
        counter = 0
        while counter < stop:
            status = self.get_resource_status(rs_id, api_ver)
            if status == 'Succeeded':
                break
            else:
                time.sleep(2)
                counter = counter + 2
                

if __name__ == "__main__":
  
    try:
        one = AZConnection(client_id=context['client_id'],
                           client_secret=context['client_secret'],
                           subscription_id=context['subscription_id'],
                           tenant_id=context['tenant_id'],
                           resource_group=context['resource_group'],
                           location=context['location'])

        subnet = one.subnet_create(virt_net_name=context['virt_net_name'],
                                   subnet_name=context['subnet_name'],
                                   ip_prefix=context['subnet_ip_prefix'])
        snet_id = subnet['id']
        one.get_status_loop(snet_id, '2020-05-01')
        status = one.get_resource_status(snet_id, '2020-05-01')

    except ConnectionError:
        ret = MSA_API.process_content('WARNING',
                                      f'Connection Error - Check Internet',
                                      context, True)
        print(ret)
        exit()
    except HTTPError:
        ret = MSA_API.process_content('WARNING',
                                      f'HTTP Error - Check API',
                                      context, True)
        print(ret)
        exit()
    
    context['snet_id'] = snet_id

    ret = MSA_API.process_content('ENDED', f'{context["virt_net_name"]} = {status}', context, True)
    print(ret)