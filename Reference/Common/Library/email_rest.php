<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * curl -u ncroot:ubiqube  -XPOST
 * 'http://localhost:10080/ubi-api-rest/email/send?from=abc@email.com&to=xyz@email.com,pqr@email.com&subject=abc&content=hello&cc=xx@email.com&bcc=yy@email.com'
 */
function _email_send ($from, $to, $subject = "", $content = "", $cc = "", $bcc = "") {

	$subject = urlencode($subject);
	$msa_rest_api = "email/send?from={$from}&to={$to}&subject={$subject}&cc={$cc}&bcc={$bcc}";
	$email_content = "";
	if ($content !== "") {
		$email_content = array('content' => $content);
		$email_content = json_encode($email_content);
	}
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $email_content);
	$response = perform_curl_operation($curl_cmd, "SEND EMAIL");
	return $response;
}

?>
