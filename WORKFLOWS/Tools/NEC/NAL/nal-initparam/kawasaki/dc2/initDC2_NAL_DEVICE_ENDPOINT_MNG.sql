insert into NAL_DEVICE_ENDPOINT_MNG
(create_id, create_date, update_id, update_date, delete_flg, extension_info)
values
('system', now(), 'system', now(), 0,
'{
	"type":"1",
	"dc_id":"system",
	"pod_id":"pod0001",
	"region_id":"",
	"endpoint_info":"
	{
		"endpoint":"http://10.169.245.33:5000/v3",
		"user_id":"admin",
		"user_password":"admin",
		"user_key":"9692ef12726d443bbd814f54d85f1fb9",
		"role_id":"0e81a51e52a64b4a8b5df4272f3f1097",
		"admin_tenant_name":"admin",
		"admin_tenant_id":"028d0efd0a4a431e9c75c642a2cbd74d",
		"openstack_keystone_ip_address":"10.169.245.33",
		"openstack_controller_node_ip_address":"10.169.245.33",
		"openstack_controller_node_server_login_id":"heat-admin",
		"openstack_controller_node_server_login_password":"P@ssw0rd",
		"region_id":"regionOne"
	}"
}'),
('system', now(), 'system', now(), 0,
'{
	"type":"2",
	"dc_id":"system",
	"pod_id":"",
	"region_id":"RegionDC2",
	"endpoint_info":"
	{
		"endpoint":"http://10.169.5.43:5000/v3/",
		"user_id":"admin",
		"user_password":"f4c6ad669c65c12e6701f2af04b6b2d598b21ed3"
	}"
}'),
('system', now(), 'system', now(), 0,
'{
	"type":"3",
	"dc_id":"system",
	"pod_id":"pod0001",
	"region_id":"",
	"endpoint_info":"
	{
		"endpoint":"https://10.169.245.64/webapi/%MSA_CLASS_NAME%?",
		"rest_endpoint":"http://10.169.245.64",
		"user_id":"ncroot",
		"user_password":"ubiqube",
		"customer_create_endpoint":"UserWS",
		"device_create_endpoint":"DeviceWS",
		"init_provisioning_endpoint":"DeviceWS",
		"object_attach_endpoint":"DeviceConfigurationWS",
		"object_execute_endpoint":"OrderCommandWS",
		"hostname_setting_endpoint":"DeviceFieldsWS",
		"ip_address":"10.169.245.64",
		"login_id":"root",
		"login_password":"root123",
		"nal_rsa_pub_dir":"/var/log/nal/job",
		"generatekey_command_path":"/home/admin/generateKey.sh",
		"movekey_command_path":"/home/admin/moveKey.sh"
	}"
}'),
('system', now(), 'system', now(), 0,
'{
	"type":"4",
	"dc_id":"system",
	"pod_id":"",
	"region_id":"RegionDC2",
	"endpoint_info":"
	{
		"endpoint":"10.169.2.20",
		"user_id":"necadmin",
		"user_password":"P@ssw0rd",
		"timeout":"300"
	}"
}');
