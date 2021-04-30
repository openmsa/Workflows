This WF is used to convert some YANG files into one Micro Service
It can convert many selected YANG files together into one xml file and after create one Micro Service

If your YANG files need some the generic library dependency, you should put all generic library dependency files into the same directorie as your YANG files.

The YANG file should be by default in the directory '/opt/fmc_repository/Datafiles/YANG'
The temporary output xml will be created in the same directory.
Click at first on 'Create Converter Instance' to create on WF instance. And after click on 'Convert Yang files to MicroService' to convert YANG files into Micro Service. 


Login to a live MSA as root and perform the following:

  cd /opt/fmc_repository
  git clone https://github.com/openmsa/Workflows OpenMSA_WF
  chown -R ncuser. OpenMSA_WF/
  cd /opt/fmc_repository/Process
  ln -sfn ../OpenMSA_WF/Convert_YANG_To_MicroService Convert_YANG_To_MicroService

Browse to the MSA GUI, open "Manage Repository".

The new entry "OpenMSA" should be available and browsable under `Automation > Workflows`.

The WF path should be /opt/fmc_repository/Process/Convert_YANG_To_MicroService/
