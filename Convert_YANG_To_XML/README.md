This WF is used to convert some YANG files into XML files.
It can convert many selected YANG files together into one xml file

If you want to convert some Cisco ConfD YANG files, you have to install first the ConfD librairie :
   Download confd-basic-7.5.1.linux.x86_64.zip or newer from https://developer.cisco.com/site/confD/downloads/   
   # Unzip and run to install :
   sh confd-basic-7.5.1.linux.x86_64.installer.bin /opt/yang/confd-basic
 

The YANG file should be by default in the directory '/opt/fmc_repository/Datafiles/YANG'
The output xml will be created in the same directory.
Click at first on 'Create Converter Instance' to create on WF instance. And after click on 'Convert Yang files to XML' to convert files into XML. 


Login to a live MSA as root and perform the following:

  cd /opt/fmc_repository
  git clone https://github.com/openmsa/Workflows OpenMSA_WF
  chown -R ncuser. OpenMSA_WF/
  cd Process/
  ln -s ../OpenMSA_WF/ OpenMSA

Browse to the MSA GUI, open "Manage Repository".

The new entry "OpenMSA" should be available and browsable under `Automation > Workflows`.

The WF path should be /opt/fmc_repository/Process/OpenMSA/Convert_YANG_To_XML/
