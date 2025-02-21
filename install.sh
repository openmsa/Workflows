#!/bin/bash
. /usr/share/install-libraries/il-lib.sh

pushd /opt/fmc_repository/Process || exit;
emit_step "WF tutorials"
to_link=(Tutorials BIOS_Automation Private_Cloud Ansible_integration Public_Cloud BIOS_Automation Upgrade_MSActivator)
for tl in "${to_link[@]}"
do
    emit_step $tl
    mk_wf_meta_link $tl
done

popd || exit



