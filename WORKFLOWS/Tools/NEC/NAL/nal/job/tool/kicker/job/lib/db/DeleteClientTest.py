from job.conf import config
from job.lib.db import delete


end_point = 'http://localhost:80/index.py/pnfs'
ids = [62]

client = delete.DeleteClient(config.JobConfig())
client.set_context(end_point, ids)
client.execute()
result = client.get_return_param()

print(type(result))
print(result)
