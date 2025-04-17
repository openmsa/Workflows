#!/bin/bash
. /usr/share/install-libraries/il-lib.sh

pushd /opt/fmc_repository/Process || exit;
emit_step "Sample Workflows"
to_link=(BIOS_Automation Private_Cloud Public_Cloud )
for tl in "${to_link[@]}"
do
    emit_step $tl
    mk_wf_meta_link $tl
done

popd || exit



