#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#  
#  COPYRIGHT  (C)  NEC  CORPORATION  2017
#  


import argparse
import fixtures
import mock
import os
import six
import sys

from nalclient import exc
from nalclient import shell as nal_shell
from nalclient.tests.unit import utils

_old_env = None

FAKE_ENV = {'OS_NAL_URL': 'http://127.0.0.1:5000/'}


class ShellTest(utils.TestCase):
    # auth environment to use
    auth_env = FAKE_ENV.copy()

    # Patch os.environ to avoid required auth info
    def make_env(self, exclude=None):
        env = dict((k, v) for k, v in self.auth_env.items() if k != exclude)
        self.useFixture(fixtures.MonkeyPatch('os.environ', env))

    def setUp(self):
        super(ShellTest, self).setUp()
        global _old_env
        _old_env, os.environ = os.environ, self.auth_env

        global shell, _shell, assert_called, assert_called_anytime
        _shell = nal_shell.NalClientShell()
        shell = lambda cmd: _shell.main(cmd.split())

    def tearDown(self):
        super(ShellTest, self).tearDown()
        global _old_env
        os.environ = _old_env

    def shell(self, argstr, exitcodes=(0,)):
        orig = sys.stdout
        orig_stderr = sys.stderr
        try:
            sys.stdout = six.StringIO()
            sys.stderr = six.StringIO()
            _shell = nal_shell.NalClientShell()
            _shell.main(argstr.split())
        except SystemExit:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.assertIn(exc_value.code, exitcodes)
        finally:
            stdout = sys.stdout.getvalue()
            sys.stdout.close()
            sys.stdout = orig
            stderr = sys.stderr.getvalue()
            sys.stderr.close()
            sys.stderr = orig_stderr
        return (stdout, stderr)

    def test_help_unknown_command(self):
        shell = nal_shell.NalClientShell()
        argstr = 'help foofoo'
        self.assertRaises(exc.CommandError, shell.main, argstr.split())

    def test_help(self):
        shell = nal_shell.NalClientShell()
        argstr = 'help'
        actual = shell.main(argstr.split())
        self.assertEqual(0, actual)

    def test_help_on_subcommand_error(self):
        self.assertRaises(exc.CommandError, self.shell, 'help bad')

    def test_get_base_parser(self):
        test_shell = nal_shell.NalClientShell()
        actual_parser = test_shell.get_base_parser()
        description = 'description'
        expected = argparse.ArgumentParser(
            prog='nal', usage=None,
            description=description,
            epilog='See "nal help COMMAND" '
                   'for help on a specific command.',
            add_help=False,
            formatter_class=nal_shell.HelpFormatter,)

        self.assertEqual(str(expected), str(actual_parser))

    @mock.patch('nalclient.v1.client.Client')
    def test_endpoint_with_v1(self, v1_client):
        args = ('--os-nal-url http://10.58.70.11 '
                'node-get --type vfw --json-data {}')
        shell = nal_shell.NalClientShell()
        shell.main(args.split())
        assert v1_client.called
        (args, kwargs) = v1_client.call_args
        self.assertEqual('http://10.58.70.11', args[0])

    @mock.patch('nalclient.v1.client.Client')
    def test_endpoint_version_error(self, v1_client):
        # Ensure that exit code is 1 for version error. 
        try:
            args = ('--os-nal-url http://10.58.70.11/v3/ '
                    'node-get --type vfw --json-data {}')
            shell = nal_shell.NalClientShell()
            shell.main(args.split())
        except SystemExit as ex:
            self.assertEqual(1, ex.code)

    @mock.patch.object(nal_shell.NalClientShell, 'main')
    def test_shell_keyboard_interrupt(self, mock_shell):
        # Ensure that exit code is 130 for KeyboardInterrupt
        try:
            mock_shell.side_effect = KeyboardInterrupt()
            nal_shell.main()
        except SystemExit as ex:
            self.assertEqual(130, ex.code)
