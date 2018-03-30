insert into NAL_POD_MNG
(create_id, create_date, update_id, update_date, delete_flg, pod_id, extension_info)
values
('system', now(), 'system', now(), 0, 'pod0001',
'{
	"use_type":3,
	"ops_version":3,
	"weight":50,
	"region_id":"regionOne"
}');
