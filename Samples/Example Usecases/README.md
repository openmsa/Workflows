# Workflow Overview
### 1. Storm-block Auto-recovery

#### Summary 
* A use case which performs automatic recovery when a broadcast storm is detected.
* Blocks specific ports based on the syslog message from the switch.

#### Workflow Details
|Item | Description|
|--- | ---|
|Workflow Name| Storm_log.xml|
|Overview|A Workflow that uses Syslog Messages to trigger Alarm Management and detect Broadcast Storms then issues Shut and No-Shut to an Interface/Port to stop the Broadcast Storm|.
|Microservice Used| cmn_interface|	

#### Scenario
1. A loop occurrence is detected
2. Syslog message is sent to **MSA**
3. **[Log Management Controller]** Upon receiving the Syslog message from the device, **MSA** then retrieves all the necessary information and converts it into an Object.
4.  **[Device Management Controller]** From the Object, get the host configuration details and prepare the configuration for recovery, if the Loop occurred for the first time recover the CLI history
5. Push configurations to the device to shut then un-shut the affected port.

#### Workflow Actions
1. Status of affected port is confirmed by getting the running configuration.
2. Generation of CLI Command
3. Configuration Update

#### Hardware Details
|Brand|Model|Firmware|
|---|---|---|
|Cisco|Catalyst2960|12.2(58)SE1|
|Cisco|Catalyst2960+|15.0(2r)EX4|

----	

### 2. SD-WAN Dynamic PBR
#### Summary
* A use case which detects high load of WAN and secures stable communication by changing route.
* Constantly monitors the bandwidth of a router and when the threshold is exceeded it instructs the SDN controller to change the route. 

#### Workflow Details
|Item|Description|
|---|---|
|Workflow Name| PBR.xml|
|Overview|A Workflow that will automatically switch routes to prevent high loads when the the threshold is reached.|
|Microservice Used| scenarios, device_group|
	
#### Scenario
1.  **NFA (Network Flow Analyzer)**  monitors the router output bandwidth.
2. SNMP Trap Notification is sent to **MSA** once the bandwidth exceeds the threshold
3.  **MSA** issues route change instruction to the **SDN Controller**.
4.  The **SDN Controller** then issues the Route change instruction to the router
5. A communication route switch occurs
	
#### Workflow Actions
1. Open csv file that contains PBR-entry conversion data
2. Check the contents of the csv file 
3. Update scenarios microservice 
4. Once changes were committed to the microservice a route change should occur.


#### Hardware Details
|Brand|Model|Firmware|
|---|---|---|
|NEC|NFA (NetFlow Analyzer)|1.1|
|NEC|PFC (Programmable Flow Controller)|8.2|

----

### 3. Configuration Back-up using TFTP
#### Summary
* A use case which periodically collects configuration to backup a large amount of network equipment.
* Utilizes the scheduling function of **MSA** , the commands are run on each network device and the configurations are sent into a TFTP server.
	
#### Workflow Details
|Item|Description|
|---|---|
|Workflow Name| TFTP.xml|
|Overview|A Workflow that backups the configurations of switches registered to a Customer into a TFTP server in a scheduled manner|
|Microservice Used| N/A|
	
#### Scenario
1. A scheduled Workflow is created from **MSA GUI**.
2. File transfer Command preparation.
3.  **[Device Management Controller]** sends the File Transfer Command to each devices via CLI Requests.
4. The device then sends their corresponding configuration to the TFTP server to be stored.
	
#### Workflow Actions
1. Devices registered under a Customer are added into a list
2. Copy the running-configuration of all the registered devices under the Customer
3. Send all configuration into the TFTP server.

#### Hardware Details
|Brand|Model|Firmware|
|---|---|---|
|Cisco|Catalyst2960|12.2(58)SE1|
|Cisco|Catalyst2960+|15.0(2r)EX4|

----

### 4. L2SW Interface Management
#### Summary
* A use case which automatically changes the network device configuration at a specified time. 
* Utilizes the scheduling function of **MSA**, the commands are run on each network device.
	
#### Workflow Details

|Item|Description|
|---|---|
|Workflow Name| Interface.xml|
|Overview|A Workflow that changes device configurations in a scheduled manner|
|Microservice Used| cmn_interface|
	
#### Scenario
1. A scheduled Workflow is created from **MSA GUI**.
2. Register Interface Information "new configuration setting".
3. **[Device Management Controller]** sends the CLI Command to each devices.
	
#### Workflow Actions
1. New configuration sent to the device via Telnet
2. "write memory" command is issued to the device.

#### Hardware Details
|Brand|Model|Firmware|
|---|---|---|
|Cisco|Catalyst2960|12.2(58)SE1|
|Cisco|Catalyst2960+|15.0(2r)EX4|
