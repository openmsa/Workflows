# Microservice Overview
### Mircoservice : cmn_interface

#### Summary 
* A Microservice for CISCO Switches. It is used to change a Physical Port's property.

#### Microservice Details
|Item | Description|
|--- | ---|
|Microservice Filename| cmn_interface.xml|
|Microservice Display Name|cmn_interface|
|Microservice Commands| Import, Update, Delete|
|Microservice Type|CLI|
|Target Device|Cisco Catalyst|
|Workflow that uses| L2SW Interface Management, <br>Storm-block Auto-recovery|

#### Variable Definition 
|Variable name| Description|
|--- | ---|	
|Interface|Container of the Interface name, this is also the Object ID of the Microservice|
|Description|A string that contains a short description of the interface|
|Mode|A selection between 2 switchport mode <br>(Possible values : Trunk, Access)|
|Trunk vLAN|A Container/Collection of Trunk vLAN address|
|Trunk vLAN Add|A Trunk vLAN Address connected to this Interface|
|Access vLAN|A Container/Collection of Access vLAN address|
|IP|The IP Address of the Port|
|Mask|The Netmask of the Port|
|Speed|The allowed Line speed <br>(Possible values : 10,100,1000,Auto)|
|Duplex|Duplex mode <br>(Possible values : Half, Full, Auto)|
|State|The status of the Port <br>(Possible values : Shut, No-Shut)|

---

### Mircoservice : scenarios

#### Summary
* A Microservice for the PFC , It is used to change scenarios saved in the PFC. 

#### Microservice Details
|Item | Description|
|--- | ---|
|Microservice Filename| scenarios.xml|
|Microservice Display Name|scenarios_pbr|
|Microservice Commands| Import, Update|
|Microservice Type|API|
|Target Device|NEC PFC|
|Workflow that uses| SD-WAN Dynamic PBR|

#### Variable Definition 
|Variable name| Description|
|--- | ---|	
|Entry ID|Scenario ID, this is also the Object ID of the Microservice.|
|Scenario Type|The type of scenario entry <br>(Possible values : pbr, filter, qos_policymap, qos_interface, qos_class, vlan_ip).|
|Enable|Scenario enable flag <br>(Possible values : True, False).|
|Position||
|Description|A string that contains a short description of the scenario.|
|Device Group Name|A container of the device_groups that are associated with the scenario, this is an object reference to **device_groups** microservice.|
|Device Group Position||
|Parameter Group Name|A container of the parameter_groups that are associated with the scenario.|
|Parameter Group Position||

---

### Mircoservice : device_groups

#### Summary
*  A Microservice for the PFC, It is used to change device_groups saved in the PFC. 

#### Microservice Details
|Item | Description|
|--- | ---|
|Microservice Filename| device_groups.xml|
|Microservice Display Name|device_groups|
|Microservice Commands| Import, Create, Delete|
|Microservice Type|API|
|Target Device|NEC PFC|
|Workflow that uses| SD-WAN Dynamic PBR|

#### Variable Definition 
|Variable name| Description|
|--- | ---|	
|object_id| Group ID, this is also the Object ID of the Microservice.|
|description|A string that contains a short description of the device group.|
|scenario_type|The type of scenario entry <br>(Possible values : pbr, filter, qos_policymap, qos_interface, qos_class, vlan_ip).|
|position||

---

