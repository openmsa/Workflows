import json
import time
import requests
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.order import Order
from msa_sdk.msa_api import MSA_API
from msa_sdk.lookup import Lookup
from msa_sdk.device import Device

dev_var = Variables()
context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

# --------------- START OF AZConnection CLASS
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
# --------------- END OF AZConnection CLASS

# --------------- START OF AZGetVMs CLASS
class AZGetVMs(AZConnection):

    # list by resource group
    # https://docs.microsoft.com/en-us/rest/api/resources/resources/listbyresourcegroup
    def get_resources(self, subscription_id, resource_group):
        url = "https://management.azure.com/" + \
              "subscriptions/" + subscription_id + \
              "/resourcegroups/" + resource_group + \
              "/resources?api-version=2020-06-01"

        payload = {}

        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.request("GET", url, headers=headers,
                                    data=payload, verify=True)

        return response.json()

    def get_vm_interface(self, virtual_machine, subscription_id, resource_group):
        net_interface = "no"
        url = "https://management.azure.com/" + \
              "subscriptions/" + subscription_id + \
              "/resourcegroups/" + resource_group + \
              "/providers/Microsoft.Compute/virtualMachines/" + virtual_machine + \
              "/?api-version=2020-06-01"

        payload = {}

        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.request("GET", url, headers=headers,
                                    data=payload, verify=True)

        net_interface = response.json()['properties']['networkProfile']['networkInterfaces'][0]['id']

        return net_interface

    def get_net_info(self, virtual_machine, subscription_id, resource_group):
        fqdn = "no"
        # url to retrieve publicIPAddress link
        url_1 = "https://management.azure.com/" + \
                self.get_vm_interface(virtual_machine, subscription_id, resource_group) + \
                "/?api-version=2020-06-01"
        payload = {}

        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.request("GET", url_1, headers=headers,
                                    data=payload, verify=True)

        private_ip = response.json()['properties']['ipConfigurations'][0]['properties']['privateIPAddress']
        url_part = response.json()['properties']['ipConfigurations'][0]['properties']['publicIPAddress']['id']

        # url to retrieve fqdn
        url_2 = "https://management.azure.com/" + \
                url_part + \
                "/?api-version=2020-06-01"

        payload = {}

        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.request("GET", url_2, headers=headers,
                                    data=payload, verify=True)

        # if machine is not ruuning only fqdn can be retrieved
        # fqdn = response.json()['properties']['dnsSettings']['fqdn']
        # Workaround ME can be created with IP address only
        if 'ipAddress' in response.json()['properties'].keys():
            fqdn = response.json()['properties']['ipAddress']
        else:
            fqdn = response.json()['properties']['dnsSettings']['fqdn']

        return fqdn, private_ip

    def get_virtual_machines(self, subscription_id, resource_group):
        vms = []
        data = self.get_resources(subscription_id, resource_group)
        for item in data['value']:
            if item['type'] == "Microsoft.Compute/virtualMachines":
                net_info = self.get_net_info(item['name'],
                                             subscription_id,
                                             resource_group)
                vm = {item['name']: {'external': net_info[0],
                                     'internal': net_info[1]
                                     }
                      }
                vms.append(vm)
        return vms
# --------------- END OF AZGetVMs CLASS

# --------------- START OF AZDelete CLASS
class AZDelete(AZConnection):

    # https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/delete
    def delete_vm(self, vm_name):

        url = self.compute_base_url + \
              "/virtualMachines/" + str(vm_name) + \
              "?api-version=2020-06-01"

        payload = {}

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("DELETE", url, headers=headers,
                                    data=payload, verify=True)

        return response.status_code, response.text

    # https://docs.microsoft.com/en-us/rest/api/compute/disks/delete
    def delete_disk(self, disk_name):

        url = self.compute_base_url + \
              "/disks/" + str(disk_name) + \
              "?api-version=2020-06-30"

        payload = {}

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("DELETE", url, headers=headers,
                                    data=payload, verify=True)

        return response.status_code, response.text

    # https://docs.microsoft.com/en-us/rest/api/virtualnetwork/networkinterfaces/delete
    def delete_nic(self, nic_name):

        url = self.net_base_url + \
              "/networkInterfaces/" + str(nic_name) + \
              "?api-version=2020-05-01"

        payload = {}

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("DELETE", url, headers=headers,
                                    data=payload, verify=True)

        return response.status_code, response.text
      
    def delete_ip(self, public_ip_name):

        url = self.net_base_url + \
              "/publicIPAddresses/" + str(public_ip_name) + \
              "?api-version=2020-05-01"

        payload = {}

        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'
                   }

        response = requests.request("DELETE", url, headers=headers,
                                    data=payload, verify=True)

        return response.status_code, response.text
      
    def del_status(self, func, resource_name, timeout=300):
      
        counter = 0
        
        while counter < timeout:
          
            resp = func(resource_name)
            status_code = resp[0]
            # 204 - No Content - resource removed or does not exist
            if status_code == 204:
                break
            # 202 - Accepted - resource removal in process
            elif status_code == 202:
                continue
            else:
                break
            time.sleep(10)
            counter += 10
        # return response message for t-shooting purposes
        return resp[1]


# --------------- END OF AZDelete CLASS

# function for masters
def del_master_me():
    pass

# function for worker
def del_worker_me(master_prim, node_name):
    
    # (1) remove node with k8s_delete_node ms / primary master
    k8s_delete_node_data = {"object_id": "123",
                            "node_name": node_name,
                            }
    k8s_delete_node_ms = {"k8s_delete_node": {"123": k8s_delete_node_data}}
    
    order = Order(master_prim)
    order.command_execute('CREATE', k8s_delete_node_ms, timeout=300)
    
  
if __name__ == "__main__":

    if int(context["scale_lvl"]) >= 0:
        ret = MSA_API.process_content('ENDED', f'Scale-out in process. Skipping.',
                                      context, True)
        print(ret)
        exit()
    
    # from low to high index 
    stop = int(context['vm_index']) + 1
    start = stop + int(context['scale_lvl'])


    # Find master - hardcoded 'k8s-node-1'
    cust_ref = context["UBIQUBEID"]
    search = Lookup()
    search.look_list_device_by_customer_ref(cust_ref)
    device_list = search.content
    device_list = json.loads(device_list)
    
    # vms to remove from msa
    msa_rm_vm = []

    for me in device_list:
        if me['name'] == context['vm_name'] + '-1':
            master_prim = me['id']
        for item in range(start, stop):
            if me['name'] == context['vm_name'] + '-' + str(item):
                msa_rm_vm.append(me['id'])

    # (1) drain and remove node from k8s cluster
    # primary master hardcoded
    try:
        for item in range(start, stop):

            node_name = context['vm_name'] + '-' + str(item)
            Orchestration.update_asynchronous_task_details(*async_update_list,
                                                           f'Removing {node_name} from k8s cluster...')
            
            del_worker_me(str(master_prim), node_name)
            
            Orchestration.update_asynchronous_task_details(*async_update_list,
                                                           f'{node_name} removed from k8s cluster.')
            
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'ERROR: {str(e)}',
                                      context, True)
        print(ret)

    # (2) remove from Azure
    try:
        one = AZDelete(client_id=context['client_id'],
                       client_secret=context['client_secret'],
                       subscription_id=context['subscription_id'],
                       tenant_id=context['tenant_id'],
                       resource_group=context['resource_group'],
                       location=context['location'])
        
        for item in range(start, stop):
            # (2.1) vm
            vm_name = context['vm_name'] + '-' + str(item)
            Orchestration.update_asynchronous_task_details(*async_update_list,
                                                           f'Removing from Azure {vm_name}...')
            time.sleep(1)
            r = one.del_status(one.delete_vm, vm_name, timeout=400)
            Orchestration.update_asynchronous_task_details(*async_update_list,
                                                           f'{r}...')
            time.sleep(10)
            # (2.2) disk
            disk_name = context['vm_name'] + '-' + str(item) + '-disk'
            Orchestration.update_asynchronous_task_details(*async_update_list,
                                                           f'Removing from Azure {disk_name}...')
            time.sleep(1)
            r = one.del_status(one.delete_disk, disk_name, timeout=400)
            Orchestration.update_asynchronous_task_details(*async_update_list,
                                                           f'{r}...')
            time.sleep(10)
            # (2.3) nic
            nic_name = context['vm_name'] + '-' + str(item) + '-nic'
            Orchestration.update_asynchronous_task_details(*async_update_list,
                                                           f'Removing from Azure {nic_name}...')
            time.sleep(1)
            r = one.del_status(one.delete_nic, nic_name, timeout=400)
            Orchestration.update_asynchronous_task_details(*async_update_list,
                                                           f'{r}...')
            time.sleep(10)
            # (2.4) ip
            ip_name = context['public_ip_name'] + '-' + str(item) + '-ip'
            Orchestration.update_asynchronous_task_details(*async_update_list,
                                                           f'Removing from Azure {ip_name}...')
            time.sleep(1)
            r = one.del_status(one.delete_ip, ip_name, timeout=400)
            Orchestration.update_asynchronous_task_details(*async_update_list,
                                                           f'{r}...')
            time.sleep(10)

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
        
    # (2) remove from MSA
    for me in msa_rm_vm:
        time.sleep(2)
        Orchestration.update_asynchronous_task_details(*async_update_list,
                                                       f'Removing from MSA {me}...')
        Device(device_id=me).delete()

    ret = MSA_API.process_content('ENDED', 'Scale-in completed.', context, True)
    print(ret)

