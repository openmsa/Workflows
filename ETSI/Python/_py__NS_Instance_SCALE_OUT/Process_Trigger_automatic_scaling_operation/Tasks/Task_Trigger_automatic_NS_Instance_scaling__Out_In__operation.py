import json
import time
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

'''
allows to get configuration variable value.
'''
def _get_configuration_variable(device, name):
    value = ''
    ret = device.get_configuration_variable(name)
    if 'value' in ret:
        value = ret.get('value')
        return value
    return ''

'''
Retrieve process instance by service instance ID.

@param orch:
    Ochestration class object reference.
@param service_id:
    Baseline workflow service instance ID.
@param timeout:
    loop duration before to break.
@param interval:
    loop time interval.
@return:
    Response of the get process instance execution.
'''
def get_process_instance(orch, process_id, timeout = 600, interval=5):
    response = {}
    global_timeout = time.time() + timeout
    while True:
        #get service instance execution status.
        orch.get_process_instance(process_id)
        response = json.loads(orch.content)
        status = response.get('status').get('status')
        #context.update(get_process_instance=status)
        if status != constants.RUNNING or time.time() > global_timeout:
            break
        time.sleep(interval)

    return response

if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('customer_id', var_type='String')
    dev_var.add('device_id', var_type='Device')
    dev_var.add('rawlog', var_type='String')
    context = Variables.task_call(dev_var)
    
    #Get device id (router) from context.
    device_id = context['device_id'][3:]
    
    #Initiate orchestraction object.
    ubiqube_id = context['UBIQUBEID']
    orch = Orchestration(ubiqube_id)
    
    #Initiate Device object
    device = Device(device_id=device_id)
    
    #Static Routing Management WF service name constant variable.
    SERVICE_NAME = 'Process/Telekom_Malaysia/_py__NS_LCM__NSD_based-on_SOL001_/_py__NS_LCM__NSD_based-on_SOL001_'
    SCALE_OUT_PROCESS_NAME = 'Process/Telekom_Malaysia/_py__NS_LCM__NSD_based-on_SOL001_/Process_Scale-out_NS'
    service_id = ''
    service_ext_ref = ''
    
    #Prepare the NS LCM WF scale out input parameter as API body.
    
    aspectId = "vsrx" #this value is defined in the NS Descriptor (.csar file).
    numberOfSteps = "1" #Default value.
    
    data = dict(aspectId=aspectId, numberOfSteps=numberOfSteps)
    
    if isinstance(data, dict):
        try:
            config_var_nslcm_wf_service_instance_ref = "nslcm_wf_service_instance_ref"
            service_ext_ref = _get_configuration_variable(device, config_var_nslcm_wf_service_instance_ref)
            context.update(config_var_nslcm_wf_service_instance_ref=config_var_nslcm_wf_service_instance_ref)
        except:
            MSA_API.task_error('nslcm service instance reference variable (' + config_var_nslcm_wf_service_instance_ref + ') is missing from ME=' + device_id, context, True)
        
        if not service_ext_ref:
            MSA_API.task_error('NS LCM Service instance reference is missing from ME config vars: id=' + device_id, context, True)
        #execute service by ref.
        orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, SCALE_OUT_PROCESS_NAME, data)
        response = json.loads(orch.content)
        context.update(nslcm_response=response)
        service_id = response.get('serviceId').get('id')
        process_id = response.get('processId').get('id')
        #get service process details.
        response = get_process_instance(orch, process_id)
        status = response.get('status').get('status')
        details = response.get('status').get('details')
        if status == constants.FAILED:
            MSA_API.task_error('Execute service operation is failed: ' + details + ' (#' + str(service_id) + ')', context, True)
        
    MSA_API.task_success( 'NS Instance SCALE_OUT operation is successfully executed.', context, True)
