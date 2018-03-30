import json

from job.conf import config
from job.lib.db import list


end_point = 'http://localhost:80/api_rest/index.py/pnfs'
ids = []
params = {
#           'delete_flg': 0,
#           'type': 1,
        'device_type': 2,
#         'status': 3,
#           'device_id': 'dev0001',
#           'redundant_configuration_flg': 1,
#           'device_name_master': 'master001',
#           'actsby_flag_master': 'act001',
#           'device_detail_master': 'detail001',
#           'master_ip_address': '10.0.0.1'
}

# for val in ids:
#     end_point += '/' + str(val)

# query = ''
# for key in params:
#     if len(query) > 0:
#         query += '&'
#     else:
#         query = '?'
#     query += key + '=' + str(params[key])
#
# end_point += query


client = list.ListClient(config.JobConfig())
client.set_context(end_point, params)
client.execute()
result = client.get_return_param()

print(type(result))
print(result)
print(type(json.dumps(result)))
print(json.dumps(result))
