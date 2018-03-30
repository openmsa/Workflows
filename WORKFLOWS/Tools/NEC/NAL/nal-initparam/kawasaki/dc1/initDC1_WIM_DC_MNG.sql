insert into WIM_DC_MNG
(create_id, create_date, update_id, update_date, dc_id, extension_info)
values
('system', now(), 'system', now(), 'dc01',
'{
	"dc_name":"DC1",
	"dc_number":"1"
}'),
('system', now(), 'system', now(), 'dc02',
'{
	"dc_name":"DC2",
	"dc_number":"2"
}'),
('system', now(), 'system', now(), 'dc03',
'{
	"dc_name":"DC3",
	"dc_number":"3"
}');
