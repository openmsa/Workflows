Templates application over multiple devices
===========================================

via auto-generated workflows.
   

Overview
--------

The demo workflow in this directory shows how a configuration
can be applied to multiple devices.
   
The effective device configuration is built from standard
MSA Micro-Services, which are attached to target devices
with an auto-generated Workflow.
   
The auto-generated Workflow is built using a "Workflow template"
in `WORKFLOWS/Utils/MSA_Template_Multi_Devices/`


Running an example
------------------

1. Create a "MSA Template" Workflow
2. Choose a Micro-Service file e.g. `FORTINET/FortigateVA/basic_conf/timezone`
3. Select Your customer ID
4. Click on Run Now

This creates a new Worflow in the repository,
called (in this case) `FORTINET_FortigateVA_basic_conf_timezone`,
under `MSA_MD_Template_Workflow`.

The auto-generated workflow features a single action: `timezone`

5. Add a new workflow `FORTINET_FortigateVA_basic_conf_timezone`
6. Create an instance. You will be prompted for Devices
7. Add all devices where you need to apply this configuration.
8. Open this workflow, and hit the button, in our exemple 'timezone'. You will be prompted with configuration parameters.
9. Click 'Run Now' and the configuration will applied


Note: the "WF-generator" workflow "MSA Template" features the following operation:
- `Refresh MSA Template Worflow`: rebuilds the workflow (same operation as create)
- `Clean MSA Template Workflow`: removes files from drive.
