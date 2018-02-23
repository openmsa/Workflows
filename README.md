# Workflows-Microservices
This repository provides some Workflows and Microservices examples.
Download them and then load them into the corresponding MSActivator repositories. 

Alternatively, see below "Installing this repo on a live MSA".


# Getting started
The [wiki](https://github.com/ubiqube/Workflows-Microservices/wiki)provides a set of tutorials to help getting started with Workflow and Microservices


Installing this repo on a live MSA
==================================

Login to a live MSA as root and perform the following:

	cd /opt/fmc_repository
	git clone https://github.com/openmsa/Workflows-Microservices.git OpenMSA
	chown -R ncuser. OpenMSA/
	cd CommandDefinition/
	ln -s ../OpenMSA/MICROSERVICES/ OpenMSA
	cd ..
	cd Process/
	ln -s ../OpenMSA/WORKFLOWS/ OpenMSA


Browse to the MSA GUI, open "Manage Repository".

Two new "OpenMSA" entries should be available and browsable
under `Workflows > OpenMSA`  and `Micro services > OpenMSA`
