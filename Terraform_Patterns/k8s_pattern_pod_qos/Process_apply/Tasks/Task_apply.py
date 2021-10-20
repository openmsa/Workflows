import os
import uuid
from shutil import copyfile
from pathlib import Path

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":
    
    dev_var = Variables()
    dev_var.add('config_path')
    dev_var.add('namespace')
    dev_var.add('config_context')
    dev_var.add('insecure')
    dev_var.add('pod_name')
    dev_var.add('container_name')
    dev_var.add('image')
    dev_var.add('requests.0.cpu')
    dev_var.add('requests.0.memory')
    dev_var.add('limits.0.cpu')
    dev_var.add('limits.0.memory')
    dev_var.add('labels.0.terrafrom')
    dev_var.add('labels.0.app')
    context = Variables.task_call(dev_var)
    
    # (0) pre check
    work_dir = os.path.dirname(os.path.realpath(__file__))
    k8s_config = Path(work_dir+"/k8s-config")
    if not k8s_config.is_file():
        ret = MSA_API.process_content('WARNING', f'PLEASE UPLOAD K8S CONFIG FILE HERE {work_dir}', context, True)
        print(ret)
        exit()
    
    # (1) create directoty
    dir_path = "/tmp/" + uuid.uuid4().hex
    context["dir_path"] = dir_path
    try:
        os.mkdir(dir_path)
    except OSError:
        ret = MSA_API.process_content('WARNING', f'CAN\'T CREATE DIRECTORY: {e}', context, True)
        print(ret)
        exit()

    
    # (2) copy files into newly created directory
    context["work_dir"] = work_dir
    try:
        copyfile(work_dir+"/k8s-config", dir_path+"/k8s-config")
        copyfile(work_dir+"/pod-qos.tf", dir_path+"/pod-qos.tf")
        copyfile(work_dir+"/provider.tf", dir_path+"/provider.tf")
    except Exception as e:
        ret = MSA_API.process_content('WARNING', f'CAN\'T COPY FILES: {e}', context, True)
        print(ret)
        exit()

    # (3) terrafrom init
    try:
        stream = os.popen(f'terraform -chdir="{dir_path}" init')
        plain_text_1 = stream.read().strip("\n")
    except Exception as e:
        ret = MSA_API.process_content('WARNING', f'CAN\'T INIT TERRAFORM: {e}', context, True)
        print(ret)
        exit()
    
    # (4) terrafrom plan
    config_path        = context["config_path"]
    namespace          = context["namespace"]
    config_context     = context["config_context"]
    insecure           = str(context["insecure"]).lower()
    pod_name           = context["pod_name"]
    container_name     = context["container_name"]
    image              = context["image"]
    requests_0_cpu     = context["requests"][0]["cpu"]
    requests_0_memory  = context["requests"][0]["memory"]
    limits_0_cpu       = context["limits"][0]["cpu"]
    limits_0_memory    = context["limits"][0]["memory"]
    labels_0_terrafrom = context["labels"][0]["terrafrom"]
    labels_0_app       = context["labels"][0]["app"]
    
    
    t4m_options = "-var='config_path=" + config_path + "' " + \
        "-var='namespace=" + namespace + "' " + \
        "-var='config_context=" + config_context + "' " + \
        "-var='insecure=" + insecure + "' " + \
        "-var='pod_name=" + pod_name + "' " + \
        "-var='container_name=" + container_name + "' " + \
        "-var='image=" + image + "' " + \
        "-var='requests={\"cpu\":\"" + requests_0_cpu + "\",\"memory\":\"" + requests_0_memory + "\"}' " + \
        "-var='limits={\"cpu\":\"" + limits_0_cpu + "\",\"memory\":\"" + limits_0_memory + "\"}' " + \
        "-var='labels={\"terraform\":\"" + labels_0_terrafrom + "\",\"app\":\"" + labels_0_app + "\"}' " + \
        "-out t4m_plan"

    try:
        stream = os.popen(f'terraform -chdir="{dir_path}" plan {t4m_options}')
        plain_text_2 = stream.read().strip("\n")
    except Exception as e:
        ret = MSA_API.process_content('WARNING', f'CAN\'T PLAN TERRAFORM: {e} {t4m_options}', context, True)
        print(ret)
        exit()
    
    # (5) terrafrom apply

    try:
        stream = os.popen(f'terraform -chdir="{dir_path}" apply "t4m_plan"')
        plain_text_3 = stream.read().strip("\n")
    except Exception as e:
        ret = MSA_API.process_content('WARNING', f'CAN\'T APPLY TERRAFORM PLAN: {e}', context, True)
        print(ret)
        exit() 

    ret = MSA_API.process_content('ENDED', f'{dir_path} :: {plain_text_1} :: {plain_text_2} :: {plain_text_3}', context, True)
    print(ret)
