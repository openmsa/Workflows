'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.

'''
import pexpect
import tempfile
import sys

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()

dev_var.add('host', var_type='String')
dev_var.add('username', var_type='String')
dev_var.add('password', var_type='String')
dev_var.add('quickstartDir', var_type='String')




def ssh(host, cmd, user, password, timeout=30, bg_run=False):
    """SSH'es to a host using the supplied credentials and executes a command.
    Throws an exception if the command doesn't return 0.
    bgrun: run command in the background"""

    fname = tempfile.mktemp()
    fout = open(fname, 'w')

    options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'
    if bg_run:
        options += ' -f'
    ssh_cmd = 'ssh %s@%s %s "%s"' % (user, host, options, cmd)
    child = pexpect.spawn(ssh_cmd, timeout=timeout)  #spawnu for Python 3
    child.expect(['[pP]assword: '])
    child.sendline(password)
    child.logfile = sys.stdout.buffer
    child.expect(pexpect.EOF)
    child.close()
    fout.close()

    fin = open(fname, 'r')
    stdout = fin.read()
    fin.close()

    if 0 != child.exitstatus:
        raise Exception(stdout)

    return stdout


context = Variables.task_call(dev_var)


ssh(context['host'], "cd "+str(context['quickstartDir'])+"; docker-compose up > /dev/null 2>&1; ", context['username'], context['password'])


ret = MSA_API.process_content('ENDED', 'Upgraded successfully', context, True)
print(ret)
