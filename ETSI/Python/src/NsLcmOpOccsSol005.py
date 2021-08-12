import json
import requests
import base64
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from custom.ETSI.BaseApi import BaseApi


class NsLcmOpOccsSol005(BaseApi):

    NS_LCM_PO_OCCS = "sol005/nslcm/v1/ns_lcm_op_occs"

    def ns_lcm_op_occs_operation_status_get(ns_lcm_op_occ_id):
        _url = self.NS_LCM_PO_OCCS + "/" + ns_lcm_op_occ_id
        response = do_get(_url)
        return response

    def ns_lcm_op_occs_completion_wait(ns_lcm_op_occ_id, timeout=60):
        ns_lcm_op_occs = self.ns_lcm_op_occs_operation_status_get(ns_lcm_op_occ_id)
        state          = ns_lcm_op_occs.json()['operationState']
        pass
