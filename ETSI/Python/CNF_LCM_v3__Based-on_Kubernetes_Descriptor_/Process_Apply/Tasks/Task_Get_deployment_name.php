<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/ETSI-MANO/KUBERNETES/utility.php';

/**
 * List all the parameters required by the task
 */
function list_args(){}

$response = $context['deploy_response'];

if ($context['resource'] == 'deployments') {
   preg_match('/\\"name\\":\s+\\"(.*)\\",\\n\s+\\"namespace\\"/', $response, $matches);
   $deployment_name = $matches[1];
   $context['deployment_name']=$deployment_name;
   task_exit(ENDED, 'Deployment name: ' . $deployment_name . '.');
} elseif ($context['resource'] == 'services') {
   preg_match('/\\"name\\":\s+\\"(.*)\\",\\n\s+\\"namespace\\"/', $response, $matches);
   $load_balancer_service_name = $matches[1];
   $context['load_balancer_service_name']=$load_balancer_service_name;
   $context['service_lb_name']=$load_balancer_service_name;
   task_exit(ENDED, 'Service name: ' . $load_balancer_service_name . '.');
}

task_exit(ENDED, 'Task ended.');

?>