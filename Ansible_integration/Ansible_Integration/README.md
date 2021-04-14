# Ansible integration
## Description
The workflow is proposed to retrive playbooks from Ansible server, created MSA microservices based on imported playbooks and attach them to Ansible server ME. After that, the microservices could be used to execute playbooks on Ansible server directlly via GUI, by 3rd party automation tools via MSA REST API or in MSA automation workflows.
## Integration options
The workflow support the following integration options:
 - **Import a playbook**          The integration allows user to create a MSA microservice based on a specific playbook;
 - **Import specific playbooks**  The integration allows user to create a few MSA microservices based on specific playbooks. Also, there is option to monitor changes in the playbooks and modyfy MSA microservices respectively; 
 - **Import all playbooks**      The integration allows to create MSA miscroservices based on all playbooks what located in specific directory. Also, there is option to monitor changes in the playbooks and modyfy MSA microservices respectively;
 
