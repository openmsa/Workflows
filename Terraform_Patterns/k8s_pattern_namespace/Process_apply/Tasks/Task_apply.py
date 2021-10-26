import os
import uuid
from shutil import copyfile
from pathlib import Path

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":
    
    dev_var = Variables()
    dev_var.add('config_path')
    dev_var.add('namespace_name')
    dev_var.add('config_context')
    dev_var.add('insecure')
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
        copyfile(work_dir+"/namespace.tf", dir_path+"/namespace.tf")
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
    namespace_name     = context["namespace_name"]
    config_context     = context["config_context"]
    insecure           = str(context["insecure"]).lower()
    labels_0_terrafrom = context["labels"][0]["terrafrom"]
    labels_0_app       = context["labels"][0]["app"]
    
    
    t4m_options = "-var='config_path=" + config_path + "' " + \
        "-var='namespace_name=" + namespace_name + "' " + \
        "-var='config_context=" + config_context + "' " + \
        "-var='insecure=" + insecure + "' " + \
        "-var='labels={\"pattern\":\"namespace\",\"terraform\":\"" + labels_0_terrafrom + "\",\"app\":\"" + labels_0_app + "\"}' " + \
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
