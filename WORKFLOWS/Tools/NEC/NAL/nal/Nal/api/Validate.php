<?php
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#  
#  COPYRIGHT  (C)  NEC  CORPORATION  2017
#  
/**
 * 1.SYSTEM   : API Controller
 * 2.FUNCTION : Validate.php
 */

require_once 'Nal/parameterCheck/message.php';

class neccsNal_validate {

    /**
     * Exec validation
     *
     * @param Input Parameters
     * @param HTTP method
     */
    public function _execValidate( $param, $method ){

        // Get a JSON file
        $vali_file = 'rule_'. $param['scenario']. '_'. $method. '_'. $param['function_type']. '.json';
        // If the JSON file exists
        if( file_exists( VALI_DIR. '/'. $vali_file ) ){

            // Get the JSON information
            $valiList = file_get_contents( VALI_DIR. '/'. $vali_file );

            $message = array();
            $valiList = json_decode( $valiList, true );

            // If you can not decode, to error
            if( empty( $valiList ) ){
                return strtr( message_Config::$valiMsg['json'], array( '%FILE%' => VALI_DIR. '/'. $vali_file )) ;
            }

            // Implement the acquired validation that is specified in the JSON file
            foreach( $valiList as $key => $vali ){

                // If there is a key "case" in the JSON file, an individual check is made
                if ( array_key_exists('case', $vali) ) {

                    $valiList = $this->_caseCheckVali( $param, $vali );

                    // Do not check if there is no parameter
                    if( empty( $vali ) ){
                        continue;
                    }

                    try{
                        foreach( $valiList as $vali ){
                            // Run the validation check
                            $this->rule( $param, $vali );
                        }

                    } catch ( Exception $e ) {
                        $message[] = $e->getMessage();
                    }

                } else if( array_key_exists('default', $vali) ){
                    continue;
                } else {

                    try{
                        // Run the validation check
                        $this->rule( $param, $vali );

                        // If an error in the validation check, get an error message
                    } catch ( Exception $e ) {
                        $message[] = $e->getMessage();
                    }

                }
            }

        // If the JSON file does not exist
        }else{
            return strtr( message_Config::$valiMsg['file'], array( '%FILE%' => VALI_DIR. '/'. $vali_file ));
        }

        // If there is more than one message, connected by a pipe(|)
        $error_message = implode("|", $message);

        return $error_message;
    }

    /**
     * Common check
     * (need to check,Minimum value check,Maximum value check)
     * and call of individual check
     *
     * @param Input Parameters
     * @param Validation check parameters
     *
     */
    protected function rule( $param, $vali ){

        // need to check
        $this->required( $param, $vali );

        $key = $vali['param'];

        $min = isset( $vali['min'] ) ? $vali['min'] : '';
        // Not essential, if the data is also empty, the end of the check
        if( $min === '' && ( !isset( $param[$key] ) || $param[$key] === '' ) ){
            return;
        }

        // Minimum value check
        $this->min( $param, $vali );

        // Maximum value check
        $this->max( $param, $vali );

        // Execution of the individual check
        $valiMethod = mb_strtolower( $vali['rule'] );
        $this->$valiMethod( $param, $vali );

    }

    /**
     * Need to check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function required( $param, $vali ){

        // Do not process if mandatory specified parameter is not available
        if( !isset( $vali['require'] ) ){
            return;
        }

        $key         = $vali['param'];
        $requireList = $vali['require'];

        $check_flg = 0;
        foreach( $requireList as $require ){
            $require_key     = $require['key'];
            $require_pattern = $require['pattern'];

            // Do not check if there are no required parameters or different values
            if( !isset( $param[$require_key] ) || !preg_match( $require_pattern, $param[$require_key] ) ){
                return;
            }
        }

        // If there is a mandatory parameter, an error if there is no data
        if( !isset( $param[$key] ) || $param[$key] === '' ){
            $message = strtr( message_Config::$valiMsg['require'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

    }

    /**
     * Minimum value check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function min( $param, $vali ){

        $key = $vali['param'];
        $value = isset( $param[$key] ) ? $param[$key] : '' ;
        $min = isset( $vali['min'] ) ? $vali['min'] : '' ;

        // Get the number of the acquired character string
        $strCount = mb_strlen( rtrim( $value ), 'UTF-8' );

        // If the number of characters in the parameter is greater than the minimum value, to error
        if( $min !== '' && $min > $strCount ){
            $trace = array(
                '%KEY%' => $key,
                '%MIN%' => $min
            );
            $message = strtr( message_Config::$valiMsg['min'], $trace );
            throw new Exception( $message );
        }
    }

    /**
     * Maximum value check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function max( $param, $vali ){

        $key = $vali['param'];
        $value = isset( $param[$key] ) ? $param[$key] : '' ;
        $max = isset( $vali['max'] ) ? $vali['max'] : '' ;

        // Get the number of the acquired character string
        $strCount = mb_strlen( rtrim( $value ), 'UTF-8' );

        // If the number of characters in the parameter is greater than the maximum value, to error
        if( $max !== '' && $max < $strCount ){
            $trace = array(
                '%KEY%' => $key,
                '%MAX%' => $max
            );
            $message = strtr( message_Config::$valiMsg['max'], $trace );
            throw new Exception( $message );
        }
    }

    /**
     * Single-byte number Check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function number( $param, $vali ){

        $key = $vali['param'];
        $value = isset( $param[$key] ) ? $param[$key] : '' ;

        if ( $value !== '' && !(preg_match( '/^[0-9]*$/D', $value )) ) {
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

    }

    /**
     * Alphabetic characters check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function alphabet( $param, $vali ){

        $key = $vali['param'];
        $value = isset( $param[$key] ) ? $param[$key] : '' ;

        if ( $value !== '' && !(preg_match( '/^[A-Za-z]*$/D', $value )) ) {
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

    }

    /**
     * Byte symbols check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function sign( $param, $vali ){

        $key = $vali['param'];
        $value = isset( $param[$key] ) ? $param[$key] : '' ;

        if ( $value !== '' && !(preg_match( '/^[\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]*$/D', $value )) ) {
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

    }

    /**
     * Alphanumeric check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function num_alpha( $param, $vali ){

        $key = $vali['param'];
        $value = isset( $param[$key] ) ? $param[$key] : '' ;

        if ( !(preg_match( '/^[0-9A-Za-z]*$/D', $value )) ) {
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }
    }

    /**
     * Alphanumeric symbol check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function num_alpha_sign( $param, $vali ){

        $key = $vali['param'];
        $value = isset( $param[$key] ) ? $param[$key] : '' ;

        if ( !(preg_match( '/^(?:[0-9A-Za-z\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]*)$/D', $value ) ) ) {
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

    }

    /**
     * String check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function string( $param, $vali ){
        // Mandatory check, minimum value check, the maximum value check
    }

    /**
     * Pattern matching check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function match( $param, $vali ){

        $key = $vali['param'];
        $pattern = $vali['pattern'];
        $value = isset( $param[$key] ) ? $param[$key] : '' ;

        if ( $value !== '' && !(preg_match( $pattern, $value )) ) {
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

    }

    /**
     * IP address check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function ip_address( $param, $vali ){

        $key = $vali['param'];
        $ip = isset( $param[$key] ) ? $param[$key] : '' ;

        // If the IP address information can not be acquired, the error
        if( !preg_match( '/^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/', $ip )){
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

    }

    /**
     * IP address IPv6 check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function ip_address_ipv6( $param, $vali ){

        $key = $vali['param'];
        $ip = isset( $param[$key] ) ? $param[$key] : '' ;

        // If the IP address information can not be acquired, the error
        if( !( filter_var( $ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6 )) ){
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

    }

    /**
     * IP address IPv4 IPv6 check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function ip_address_ipv4v6( $param, $vali ){

        $key = $vali['param'];
        $ip = isset( $param[$key] ) ? $param[$key] : '' ;

        $ipv4_check = 0;
        $ipv6_check = 0;

        try{
            $this->ip_address( $param, $vali );
        } catch ( Exception $e ) {
            $ipv4_check = 1;
        }

        try{
            $this->ip_address_ipv6( $param, $vali );
        } catch ( Exception $e ) {
            $ipv6_check = 1;
        }

        if( $ipv4_check === 1 && $ipv6_check === 1 ){
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

    }

    /**
     * Network address check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function network_address( $param, $vali ){

        $key = $vali['param'];
        $value = isset( $param[$key] ) ? $param[$key] : '' ;

        // If you do not have a "/", to error
        if( !preg_match( '/\//', $value ) ){
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

        // Divided into ip and mask portion
        list( $ip, $mask ) = explode( '/', $value );

        // Error if mask is not numeric
        if( !preg_match( '/^[0-9]+$/', $mask ) ){
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

        // Error if mask is less than 0 or greater than 32
        if( intval($mask) < 0 || intval($mask) > 32 ){
            $message = strtr( message_Config::$valiMsg['format'], array( '%KEY%' => $key ) );
            throw new Exception( $message );
        }

        $param[$key] = $ip;
        $this->ip_address( $param, $vali );

    }

    /**
     * Create validation list for individual check
     *
     * @param Input Parameters
     * @param Validation parameters
     *
     */
    protected function _caseCheckVali( $param, $vali ){

        $caseParamList = $vali['case'];
        $case_key     = '';
        $case_pattern = '';

        $param_flg = 0;
        $caseCheckVali = array();
        foreach( $caseParamList as $key => $case ){

            if ( !array_key_exists( 'case_param', $case ) ) {
                continue;
            }

            // Acquire specified parameter information
            $case_key     = $case['case_param']['case_key'];
            $case_pattern = $case['case_param']['case_pattern'];

            // If a particular parameter exists and matches a regular expression
            if( isset( $param[$case_key] ) && preg_match( $case_pattern, $param[$case_key] ) ){

                $param_flg = 1;
                $caseCheckVali[$key]['param']   = $vali['param'];
                $caseCheckVali[$key]['rule']    = $case['rule'];
                $caseCheckVali[$key]['min']     = isset( $case['min'] ) ? $case['min'] : '' ;
                $caseCheckVali[$key]['max']     = isset( $case['max'] ) ? $case['max'] : '' ;
                if( $case['rule'] === 'MATCH' ){
                    $caseCheckVali[$key]['pattern']  = $case['pattern'];
                }
            }
        }

        // If none of the conditions apply to "default" setting
        if( $param_flg === 0 && isset( $vali['default'] ) ){
            $caseCheckVali[0]['param']   = $vali['param'];
            $caseCheckVali[0]['rule']    = $vali['default']['rule'];
            $caseCheckVali[0]['min']     = isset( $vali['default']['min'] ) ? $vali['default']['min'] : '' ;
            $caseCheckVali[0]['max']     = isset( $vali['default']['max'] ) ? $vali['default']['max'] : '' ;
            if( $vali['default']['rule'] === 'MATCH' ){
                $caseCheckVali[0]['pattern']  = $vali['default']['pattern'];
            }
        }

        return $caseCheckVali;

    }
}