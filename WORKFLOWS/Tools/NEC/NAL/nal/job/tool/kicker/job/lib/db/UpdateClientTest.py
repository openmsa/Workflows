from job.conf import config
from job.lib.db import update


end_point = 'http://localhost:80/index.py/pnfs'
ids = [62]
params = {
#           'delete_flg': 0,
#           'type': 1,
#           'device_type': 2,
          'status': 4,
#           'device_id': 'dev0001',
#           'redundant_configuration_flg': 1,
#           'device_name_master': 'master001',
#           'actsby_flag_master': 'act001',
#           'device_detail_master': 'detail001',
#           'master_ip_address': '10.0.0.1'
}

client = update.UpdateClient(config.JobConfig())
client.set_context(end_point, ids, params)
client.execute()
result = client.get_return_param()

print(type(result))
print(result)
