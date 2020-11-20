VMWare VM Automation Demo using VM Templates
=========

This workflow requires a series of VM templates to be created in the VMWare Cloud before we can run this demo.
For exmaple if we choose a VM template with a name: "MY_TEMPLATE"and we want to have more than one VM for each batch of the VMs we bring in, we also need to have that many VM templates with names : "MY_TEMPLATE_1". "MY_TEMPLATE_2" ...so on.

The user will choose the base template and the batch size. This WF has hardcoded to a maximum batch size of 2.
