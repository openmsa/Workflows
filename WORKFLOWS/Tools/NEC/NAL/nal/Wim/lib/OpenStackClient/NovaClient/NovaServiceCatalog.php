<?php
/**
 * 1.SYSTEM   :
 * 2.FUNCTION : OpenStack Client nova_endpoint
 *
 * @version $Id: $
 */
require_once dirname(__FILE__). '/../conf/OscConst.php';

class NovaServiceCatalog{

    /**
     * endpoint URL
     *
     * @param  session ID
     * @return keystone endpoint URL
     */
    public static function getNovaEndpoint( $endPointArray, $region_id ){

        $catalogs = array();
        $url      = '';

        $catalogs = $endPointArray['token']['catalog'];
        $service_name = 'nova';

        //end point
        foreach ( $catalogs as $catalog) {
            if ( $catalog['name'] == $service_name ){
                foreach( $catalog['endpoints'] as $endpoint ){
                    if( $endpoint['interface'] === 'admin' && $endpoint['region_id'] === $region_id ){
                        $url = $endpoint['url'];
                        break;
                    }
                }
            }
        }

        return $url;
    }

    public function getCinderEndpoint( $endPointArray ){
        //init
        $catalogs = array();
        $roles = array();
        $adminFLG = false;
        $url = '';
        //memcache
        try{
            $endpoint = $endPointArray[OscConst::KEY_ENDPOINT];
            $roles = $endpoint['access']['user']['roles'];
            $catalogs = $endpoint['access']['serviceCatalog'];

            // WIM endpoint
            $wim_flg = isset($endPointArray["wim_flg"]) ? $endPointArray["wim_flg"] : false;

            // service name
            if ( $wim_flg ) {
                $service_name1 = 'cinder';
                $service_name2 = 'nova_volume';
                $service_name3 = 'volume';
            } else {
                $service_name1 = 'cinder';
                $service_name2 = 'nova_volume';
                $service_name3 = 'volume';
            }

            //role
            foreach  ( $roles as $role) {
                if ( $role == 'admin' or 'ResellerAdmin'){
                    $adminFLG = true;
                    break;
                }
            }
            //end point
            foreach ( $catalogs as $catalog) {
                if ( $catalog['name'] == $service_name1 or $catalog['name'] == $service_name2 or $catalog['name'] == $service_name3 ){
                    if ($adminFLG == true){
                        $url = $catalog['endpoints']['0']['adminURL'];
                        break;
                    }else{
                        $url = $catalog['endpoints']['0']['publicURL'];
                        break;
                    }
                }
            }
        }catch(Exception $e ){
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_07, $e),  $e->getCode(), $e);
        }
        return $url;
    }
    public function getCinderV1_1Endpoint( $endPointArray ){

        $serviceName = array('cinder');
        return $this->getEndpoint($endPointArray, $serviceName);

    }
    public function getCinderV2Endpoint( $endPointArray ){

        $serviceName = array('cinderv2');
        return $this->getEndpoint($endPointArray, $serviceName);

    }
}
?>
