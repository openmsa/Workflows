Update Workflow Code
=================

This doc explains how to update the code of the workflows installed in your MSActivator setup.

Overview
--------

The adapters are installed in the MSActivator container msa_dev, in the directory `/opt/fmc_repository/OpenMSA_WF`.

```
[root@5512fb840172 OpenMSA_WF]# pwd
/opt/fmc_repository/OpenMSA_WF

[root@5512fb840172 OpenMSA_WF]# ll
total 72
drwxr-xr-x  3 ncuser ncuser    20 Mar 23 08:10 Analytics
drwxr-xr-x  3 ncuser ncuser    33 Mar 23 08:10 Ansible
drwxr-xr-x  2 ncuser ncuser  4096 Mar 23 08:10 Ansible_integration
drwxr-xr-x  4 ncuser ncuser    58 Mar 23 08:10 Azure_k8s
drwxr-xr-x  5 ncuser ncuser   106 Mar 23 08:10 BIOS_Automation
-rwxr-xr-x  1 ncuser ncuser   516 Mar 23 08:10 CONTRIBUTING.md
drwxr-xr-x  2 ncuser ncuser  4096 Mar 23 08:10 Compliance_Check
drwxr-xr-x  2 ncuser ncuser  4096 Mar 23 08:10 General_Network_Service_Automation
drwxr-xr-x  3 ncuser ncuser    24 Mar 23 08:10 Good_Better_Best
drwxr-xr-x  3 ncuser ncuser    25 Mar 23 08:10 Kubernetes
-rwxr-xr-x  1 ncuser ncuser 35147 Mar 23 08:10 LICENSE
drwxr-xr-x  4 ncuser ncuser    56 Mar 23 08:10 MEC
drwxr-xr-x  2 ncuser ncuser  4096 Mar 23 08:10 Microwave_station_provisioning
drwxr-xr-x  4 ncuser ncuser   231 Mar 23 08:10 Multi_Firewall
drwxr-xr-x  4 ncuser ncuser   113 Mar 23 08:10 Optical_SDN
drwxr-xr-x  6 ncuser ncuser   300 Mar 23 08:10 Password_Manager
drwxr-xr-x  3 ncuser ncuser    83 Mar 23 08:10 Private_Cloud
drwxr-xr-x  4 ncuser ncuser    48 Mar 23 08:10 Public_Cloud
-rwxr-xr-x  1 ncuser ncuser   784 Mar 23 08:10 README.md
drwxr-xr-x  6 ncuser ncuser   140 Mar 23 08:10 Reference
drwxr-xr-x  7 ncuser ncuser   226 Mar 23 08:10 Samples
drwxr-xr-x  7 ncuser ncuser  4096 Mar 23 08:10 Terraform_Configuration_Management
drwxr-xr-x  3 ncuser ncuser    60 Mar 23 08:10 Ticketing
drwxr-xr-x  8 ncuser ncuser  4096 Mar 23 08:10 Topology
drwxr-xr-x 11 ncuser ncuser  4096 Mar 23 08:10 Tutorials
drwxr-xr-x  7 ncuser ncuser   257 Mar 23 08:10 Utils
drwxr-xr-x  4 ncuser ncuser    67 Mar 23 08:10 Workload_Placement_Selection_MEC
drwxr-xr-x  3 ncuser ncuser    73 Mar 23 08:10 uCPE

[root@5512fb840172 OpenMSA_WF]# git status
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
[root@5512fb840172 OpenMSA_WF]# git remote -v
origin	https://github.com/openmsa/Workflows.git (fetch)
origin	https://github.com/openmsa/Workflows.git (push)

```

There are 2 ways of updating the adapters in your MSActivator:

- automatically with the script `install_libraries.sh` 
- manually using git commands

If you haven's done any change to your local version of the code, you should use the script. 
In case you have done some changes, then the script may not be able to automatically merge the code from github into your version of the code and you will have to manually update your git repository.

Automated update
----------------

From the directory where the docker-compose file is installed, run the command below

```
docker-compose exec msa_dev /usr/bin/install_libraries.sh wf
```

The script will take care of updating your local git repository and will attempt to merge the code from the remote master branch into your code.

If there are conflicting modification, you will have to update the repository manually.

Manual update
-------------

1 - From the directory where the docker-compose file is installed, connect to the `msa_dev` container:

```
docker-compose exec msa_dev bash
```

2 - Go to the adapter git repository:

```
 cd /opt/fmc_repository/OpenMSA_WF
 ```

 3 - Pull the latest code of the adapter which is always available on the master branch

 ```
 git pull origin master
 ```

Git may raise conflict related errors if you have some uncommited local changes. You need to either commit your changes (`git add ...` and `git commit ...`) or stash them (`git stash`)

4 - Set the user to `ncuser`

```
chown -R ncuser. *
```

Enable a new workflow
----------------------

All the community workflows available in this github repository are all installed on your MSActivator setup under `/opt/fmc_repository/OpenMSA_WF` but not all of them are enabled.

To enable a workflow, you need to install it under `/opt/fmc_repository/Process`

```
[root@5512fb840172 Process]# pwd
/opt/fmc_repository/Process

[root@5512fb840172 Process]# ll
total 0
lrwxrwxrwx 1 ncuser ncuser  23 Mar 23 08:19 Analytics -> ../OpenMSA_WF/Analytics
lrwxrwxrwx 1 ncuser ncuser  33 Mar 23 08:19 Ansible_integration -> ../OpenMSA_WF/Ansible_integration
lrwxrwxrwx 1 ncuser ncuser  29 Mar 23 08:19 BIOS_Automation -> ../OpenMSA_WF/BIOS_Automation
drwxr-xr-x 5 ncuser ncuser  97 Mar 26 09:41 Helloworld
lrwxrwxrwx 1 ncuser ncuser  27 Mar 23 08:19 Private_Cloud -> ../OpenMSA_WF/Private_Cloud
lrwxrwxrwx 1 ncuser ncuser  26 Mar 23 08:19 Public_Cloud -> ../OpenMSA_WF/Public_Cloud
drwxr-xr-x 5 ncuser ncuser 110 Mar 23 08:19 PythonReference
lrwxrwxrwx 1 ncuser ncuser  23 Mar 23 08:19 Reference -> ../OpenMSA_WF/Reference
lrwxrwxrwx 1 ncuser ncuser  69 Mar 23 08:19 SelfDemoSetup -> ../quickstart/lab/msa_dev/resources/libraries/workflows/SelfDemoSetup
lrwxrwxrwx 1 ncuser ncuser  22 Mar 23 08:19 Topology -> ../OpenMSA_WF/Topology
lrwxrwxrwx 1 ncuser ncuser  23 Mar 23 08:19 Tutorials -> ../OpenMSA_WF/Tutorials
drwxr-xr-x 7 ncuser ncuser 114 Mar 29 07:40 workflows
```

The easiest way to do that is to use symbolic link from `/opt/fmc_repository/Process` to `/opt/fmc_repository/OpenMSA_WF`.

For example, to enable the workflow `Terraform_Configuration_Management`, you can use the CLI command

```
ln -sfn ../OpenMSA_WF/Terraform_Configuration_Management Terraform_Configuration_Management
```

Make sure that you set the correct user:

```
chown -R ncuser. /opt/fmc_repository/Process/Terraform_Configuration_Management
```

