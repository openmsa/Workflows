#!/bin/sh

ID=root
PWD=i-portal
DB=nal;
dt=`date '+%Y%m%d%H%M%S'`

if [ $# -eq 1 ] ; then
        tables=$1
        tname=$1
else
        #tables="NAL_APL_MNG NAL_CONFIG_MNG NAL_LICENSE_MNG"
        tables="NAL_APL_MNG NAL_CONFIG_MNG NAL_DEVICE_ENDPOINT_MNG NAL_GLOBAL_IP_MNG NAL_LICENSE_MNG NAL_MSA_VLAN_MNG NAL_POD_MNG NAL_PORT_MNG NAL_THRESHOLD_MNG NAL_TENANT_MNG NAL_VIRTUAL_LAN_MNG NAL_VXLANGW_POD_MNG WIM_CONFIG_MNG WIM_DC_CONNECT_GROUP_MNG WIM_DC_CONNECT_MEMBER_MNG WIM_DC_MNG WIM_DC_VLAN_MNG WIM_DEVICE_ENDPOINT_MNG"
        tname="all"
fi


fn=res.${tname}.${dt}
wfn=.work

for table in $tables
do
        #sql="select extension_info from ${table} \G;"
        sql="select * from ${table} \G;"
        echo "##### ${table} ##### ${dt}" >> ${fn}
        mysql -u${ID} -p${PWD} ${DB} -e "$sql" > ${wfn}
        #cp ${wfn} ${wfn}.${table}
        #sed -i -e '1d' ${wfn}
        if [ -s zero ]; then
                echo "No Data" >> ${fn}
        else
                python2 nalshowdb_sub.py >> ${fn}
        fi
done

rm -f ${wfn}
#cat ${fn}
