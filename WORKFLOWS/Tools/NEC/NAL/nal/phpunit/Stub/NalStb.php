<?php
require_once dirname(__FILE__) . '/../../Nal/api/Nal.php';

class neccsNalStb extends neccsNal {
    protected function error( $code, $message, $out='' ) {
        throw new Exception( $message );
    }

    protected function _execApi( $url, $param='', $noproxy='' ) {

        if( preg_match('/appliances/', $url) ){

            $result[0]['create_id'] = 'system';
            $result[0]['create_date'] = '20160729000000';
            $result[0]['update_id'] = 'system';
            $result[0]['update_date'] = '20160729000000';
            $result[0]['delete_flg'] = '0';
            $result[0]['ID'] = '33';
            $result[0]['node_id'] = '123456789';
            $result[0]['tenant_name'] = 'tenant_name1';
            $result[0]['pod_id'] = '2';
            $result[0]['tenant_id'] = '1234';
            $result[0]['apl_type'] = '1';
            $result[0]['type'] = '1';
            $result[0]['device_type'] = '2';
            $result[0]['task_status'] = '1';
            $result[0]['err_info'] = '';
            $result[0]['description'] = 'memo';
            $result[0]['node_name'] = '';
            $result[0]['node_detail"'] = '';
            $result[0]['server_id'] = '';
            $result[0]['server_info"'] = '';
            $result[0]['MSA_device_id'] = '';

        }

        if( preg_match('/nal-endpoints/', $url) ){

            $result[0]['device_type'] = '1';
            $result[0]['region_id']   = '';
            $result[0]['pod_id']      = '3';
            $endpoint_info['vim']['endPoint']          = 'http://10.58.79.97:5000/v2.0';
            $endpoint_info['vim']['userId']            = 'admin';
            $endpoint_info['vim']['userPassword']      = 'admin';
            $endpoint_info['vim']['userkey']           = '2953e1c876454fc3b59a1eaf09bd7a09';
            $endpoint_info['vim']['role_id']           = 'cd034e1a0f774a1aa125edcc3f35598e';
            $endpoint_info['vim']['admin_tenant_name'] = 'admin';

            $result[0]['endpoint_info'] = json_encode( $endpoint_info );
        }

        return $result;
    }
}

