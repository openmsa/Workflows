# -*- coding: utf-8 -*-

import sys
import json
import datetime

f = open(".work")
data = f.read()
f.close()

lines = data.split('\n')
for line in lines:
    if 'extension_info: ' in line:
        print "extension_info: "
        value = line.replace('extension_info: ', '')
        #print "value"
        #print value

        #value = value.replace("\\\\", "\\")
        #print "value"
        #print value

        dict = json.loads(value)
        for key, val in dict.items():
            if '{\"' in str(val):
                dict[key] = json.loads(val)
        encode_json_data = json.dumps(dict, sort_keys=True, indent=10, separators=(',', ': '))
        print encode_json_data

    elif '***************************' in line:
        todaydetail = datetime.datetime.today()
        print line ,
        print todaydetail.strftime("%Y%m%d-%H%M%S")

    else:
        print line
