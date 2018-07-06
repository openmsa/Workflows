<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * curl -u ncroot:NCROOT_PWD  -XPOST "http://localhost:10080/ubi-api-rest/repository/operator?uri={uri}"
 */
function _repository_add_operator ($uri) {
	$msa_rest_api = "repository/operator?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY ADD OPERATOR");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XDELETE "http://localhost:10080/ubi-api-rest/repository/operator?uri={uri}"
 */
function _repository_remove_operator ($uri) {
	$msa_rest_api = "repository/operator?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY REMOVE OPERATOR");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPOST "http://localhost:10080/ubi-api-rest/repository/manufacturer?uri={uri}"
 */
function _repository_add_manufacturer ($uri) {
	$msa_rest_api = "repository/manufacturer?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY ADD MANUFACTURER");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XDELETE "http://localhost:10080/ubi-api-rest/repository/manufacturer?uri={uri}"
 */
function _repository_remove_manufacturer ($uri) {
	$msa_rest_api = "repository/manufacturer?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY REMOVE MANUFACTURER");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPOST "http://localhost:10080/ubi-api-rest/repository/model?uri={uri}"
 */
function _repository_add_model ($uri) {
	$msa_rest_api = "repository/model?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY ADD MODEL");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XDELETE "http://localhost:10080/ubi-api-rest/repository/model?uri={uri}"
 */
function _repository_remove_model ($uri) {
	$msa_rest_api = "repository/model?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY REMOVE MODEL");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPOST "http://localhost:10080/ubi-api-rest/repository/customer?uri={uri}"
 */
function _repository_add_customer ($uri) {
	$msa_rest_api = "repository/customer?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY ADD CUSTOMER");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XDELETE "http://localhost:10080/ubi-api-rest/repository/customer?uri={uri}"
 */
function _repository_remove_customer ($uri) {
	$msa_rest_api = "repository/customer?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY REMOVE CUSTOMER");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPOST "http://localhost:10080/ubi-api-rest/repository/directory?uri={uri}&tag={tag}&comment={comment}"
 */
function _repository_add_directory ($uri, $tag = "", $comment = "") {
	$msa_rest_api = "repository/operator?uri={$uri}&tag={$tag}&comment={$comment}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY ADD DIRECTORY");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XDELETE "http://localhost:10080/ubi-api-rest/repository/directory?uri={uri}"
 */
function _repository_remove_directory ($uri) {
	$msa_rest_api = "repository/directory?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY REMOVE DIRECTORY");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPOST "http://localhost:10080/ubi-api-rest/repository/file?uri={uri}&tag={tag}&comment={comment}" -d '{"content":"xyz"}'
 */
function _repository_add_file ($uri, $content, $tag = "", $comment = "") {
	$msa_rest_api = "repository/file?uri={$uri}&tag={$tag}&comment={$comment}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $content);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY ADD FILE");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPOST "http://localhost:10080/ubi-api-rest/repository/file/copy?uri={uri}&tag={tag}&comment={comment}" -d '@file_path'
 */
function _repository_copy_file ($uri, $file_path, $tag = "", $comment = "") {
	$msa_rest_api = "repository/file/copy?uri={$uri}&tag={$tag}&comment={$comment}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, "@{$file_path}");
	$response = perform_curl_operation($curl_cmd, "REPOSITORY COPY FILE");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XDELETE "http://localhost:10080/ubi-api-rest/repository/file?uri={uri}"
 */
function _repository_remove_file ($uri) {
	$msa_rest_api = "repository/file?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY REMOVE FILE");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XGET "http://localhost:10080/ubi-api-rest/repository/exists?uri={uri}"
 */
function _repository_exists ($uri) {
	$msa_rest_api = "repository/exists?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY EXISTS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPUT "http://localhost:10080/ubi-api-rest/repository/tag?uri={uri}&tag={tag}"
 */
function _repository_update_tag ($uri, $tag = "") {
	$msa_rest_api = "repository/tag?uri={$uri}&tag={$tag}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY UPDATE TAG");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPUT "http://localhost:10080/ubi-api-rest/repository/comment?uri={uri}&comment={comment}"
 */
function _repository_update_comment ($uri, $comment = "") {
	$msa_rest_api = "repository/comment?uri={$uri}&comment={$comment}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY UPDATE COMMENT");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPUT "http://localhost:10080/ubi-api-rest/repository/file?uri={uri}" -d '{"content":"xyz"}'
 */
function _repository_update_file_content ($uri, $content) {
	$msa_rest_api = "repository/file?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api, $content);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY UPDATE FILE CONTENT");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XGET "http://localhost:10080/ubi-api-rest/repository/file?uri={uri}"
 */
function _repository_read_file_content ($uri) {
	$msa_rest_api = "repository/file?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY GET FILE CONTENT");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XGET "http://localhost:10080/ubi-api-rest/repository/files?uri={uri}"
 */
function _repository_list_files ($uri) {
	$msa_rest_api = "repository/files?uri={$uri}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "REPOSITORY LIST FILES");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>