import os
import shutil

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call()
    
    # (1) destroy
    dir_path           = context["dir_path"]
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
        "-var='labels={\"pattern\":\"namespace\",\"terraform\":\"" + labels_0_terrafrom + "\",\"app\":\"" + labels_0_app + "\"}'"

    try:
        stream = os.popen(f'terraform -chdir="{dir_path}" destroy -auto-approve {t4m_options}')
        plain_text_2 = stream.read().strip("\n")
    except Exception as e:
        ret = MSA_API.process_content('WARNING', f'CAN\'T DESTROY TERRAFORM: {e} {t4m_options}', context, True)
        print(ret)
        exit()
    
    # (2) remove directoty
    try:
        # os.rmdir(dir_path)
        shutil.rmtree(dir_path)
    except OSError:
        ret = MSA_API.process_content('WARNING', 'CAN\'T REMOVE DIRECTORY', context, True)
        print(ret)
        exit()

    ret = MSA_API.process_content('ENDED', 'OK', context, True)
    print(ret)