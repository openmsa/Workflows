# Kubernetes Pod with QoS parameters

## Purposes
This is a workflow that executes terrafrom commands and uses k8s pod pattern configuration.
QoS pattern is intended to create pod that has requests and limits configuration https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits 

## Prerequisites
 - Terrafrom should be installed in msa_api container, see installation guide here https://learn.hashicorp.com/tutorials/terraform/install-cli
 - Kubernetes config file should be uploaded

## Constraints
 - Pattern creates Pod with requests and limits configured
 - Namespace (default) can be modified. But the namespace creation is out of the scope of this pattern.

## Execution order
1. Check that k8s configuration file exists - if not the WF throws message where to place that file
2. Copy files into /tmp/<temp-dir>
3. Terrafrom init in /tmp/<temp-dir>
4. Terrafrom plan passing variables from UI in /tmp/<temp-dir>
5. Terrafrom apply
6. Terrafrom destroy - in case of removing WF instances - will remove /tmp/<temp-dir> and wipe out pod
