<?php
/**
 * 1.SYSTEM   :
 * 2.FUNCTION : OpenStack initial endpoint
 *
 * @version $Id:$
 */
umask(000);

class OscConst {

    //REST HTTP METHOD
    const METHOD_GET    = 'GET';
    const METHOD_POST   = 'POST';
    const METHOD_PUT    = 'PUT';
    const METHOD_DELETE = 'DELETE';

    //memcached Key
    const MEM_TOKEN     = '_TOKEN';
    const MEM_ENDPOINT  = '_ENDPOINT';
    const MEM_TYPE      = '_keystone';

    const KEY_TOKEN     = '_TOKEN';
    const KEY_ENDPOINT  = '_ENDPOINT';

    //Exception Message
    const Exce_Message_01 = 'error args key';
    const Exce_Message_02 = 'error GET REST I/F';
    const Exce_Message_03 = 'error POST REST I/F';
    const Exce_Message_04 = 'error PUT REST I/F';
    const Exce_Message_05 = 'error DELETE REST I/F';
    const Exce_Message_06 = 'error memcached of token id';
    const Exce_Message_07 = 'error memcached of endpoint';
    const Exce_Message_08 = 'error ENDPOINT was not found. Probably, you do not have authority.';
    const Exce_Message_09 = 'error OpenStack Non Response';
    const Exce_Message_10 = 'error memcached set';
    const Exce_Message_11 = 'error update quotas';
    const Exce_Message_12 = 'error OpenStack Abnormal Response returned';

    /** Log output items **/
    const LOG_STATUS_START    = 'Start';
    const LOG_STATUS_ERROR    = 'Error';
    const LOG_STATUS_COMPLATE = 'Complete';

    const HTTP_ERRCODE_NO = 78000;

    function __construct() {
    }

    public static function Exception_message($name , $message, $e){
        return json_encode( array("ERROR" => array( "NAME" => $name, "OPENSTACK_MESSAGE" => $message, "EXCEPTION_MESSAGE" => $e)), true);
    }

}
?>
