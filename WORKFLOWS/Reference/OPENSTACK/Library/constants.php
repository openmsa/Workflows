<?php 

// Keystone Service names
define('NOVA', 'nova');
define('HEAT', 'heat');
define('CINDERV1', 'cinderv1');
define('CINDERV2', 'cinderv2');
define('GLANCE', 'glance');
define('CEILOMETER', 'ceilometer');
define('HEAT-CFN', 'heat-cfn');
define('CINDER', 'cinder');
define('EC2', 'ec2');
define('NOVAV21', 'novav21');
define('SWIFT', 'swift');
define('KEYSTONE', 'keystone');
define('NEUTRON', 'neutron');

// Template name and variable name for multi-tenancy
define('TENANT_CONTEXT_TEMPLATE', 'tenant_context');
define('TENANT_ID_VARIABLE', 'TENANT_ID');

// Openstack X-Subject-Token in respons header
define('X_SUBJECT_TOKEN', 'X-Subject-Token');

// Openstack URL Endpoint names
define('ADMIN_URL', 'adminURL');
define('INTERNAL_URL', 'internalURL');
define('PUBLIC_URL', 'publicURL');

// Openstack Server/Port Status
define('ACTIVE', 'ACTIVE');
define('BUILD', 'BUILD');
define('SHUTOFF', 'SHUTOFF');
define('RESIZE', 'RESIZE');
define('VERIFY_RESIZE', 'VERIFY_RESIZE');
define('DOWN', 'DOWN');
define('SUSPENDED', 'SUSPENDED');
define('RESUMED', 'RESUMED');

// Openstack Volume Status
define('VOLUME_CREATING', 'creating');
define('VOLUME_AVAILABLE', 'available');
define('VOLUME_ATTACHING', 'attaching');
define('VOLUME_IN_USE', 'in-use');
define('VOLUME_DELETING', 'deleting');
define('VOLUME_BACKING_UP', 'backing-up');
define('VOLUME_RESTORING_BACKUP', 'restoring-backup');
define('VOLUME_ERROR', 'error');
define('VOLUME_ERROR_DELETING', 'error_deleting');
define('VOLUME_ERROR_RESTORING', 'error_restoring');
define('VOLUME_ERROR_EXTENDING', 'error_extending');

// Poll Sleep params
define('SERVER_STATUS_CHECK_SLEEP', 10);
define('PORT_STATUS_CHECK_SLEEP', 5);
define('VOLUME_STATUS_CHECK_SLEEP', 10);

// Status Change Timeout
define('SERVER_STATUS_CHANGE_TIMEOUT', 600);
define('PORT_STATUS_CHANGE_TIMEOUT', 180);
define('VOLUME_STATUS_CHANGE_TIMEOUT', 600);

// Status Change Retry Interval
define('SERVER_STATUS_CHANGE_RETRY_INTERVAL', 180);

?>
