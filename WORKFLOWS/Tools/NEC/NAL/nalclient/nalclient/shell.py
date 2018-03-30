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


"""
Command-line interface to the OpenStack Aflo API.
"""

from __future__ import print_function

import argparse
import copy
import logging
import sys
import traceback

import nalclient as client
from nalclient import client_const
from nalclient.common import utils
from nalclient import exc

VERSION = client.__version__


class NalClientShell(object):

    def _append_global_identity_args(self, parser):
        parser.add_argument('--id-password',
                            default=utils.env('NAL_ID_PASSWORD'),
                            help=('Defaults to env[NAL_ID_PASSWORD].'))

        parser.add_argument(
            client_const.COMMAND_ARGS_OS_CLIENT_URL_NAME,
            default=utils.env(client_const.ENV_OS_CLIENT_URL_NAME),
            help=('Defaults to env[%s].' %
                  client_const.ENV_OS_CLIENT_URL_NAME))

    def get_base_parser(self):
        parser = argparse.ArgumentParser(
            prog=client_const.COMMAND,
            description='description',
            epilog='See "%s help COMMAND" '
                   'for help on a specific command.' % client_const.COMMAND,
            add_help=False,
            formatter_class=HelpFormatter,
        )

        # Global arguments
        parser.add_argument('-h', '--help',
                            action='store_true',
                            help=argparse.SUPPRESS,
                            )

        parser.add_argument('--version',
                            action='version',
                            version=VERSION)

        parser.add_argument('-d', '--debug',
                            default=bool(utils.env('CLIENT_DEBUG')),
                            action='store_true',
                            help='Defaults to env[CLIENT_DEBUG].')

        parser.add_argument('-v', '--verbose',
                            default=False, action="store_true",
                            help="Print more verbose output")

        self._append_global_identity_args(parser)

        return parser

    def get_subcommand_parser(self, version):
        parser = self.get_base_parser()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')
        try:
            submodule = utils.import_versioned_module(version, 'shell')
        except ImportError:
            print('"%s" is not a supported API version. Example '
                  'values are "1".' % version)
            utils.exit()

        self._find_actions(subparsers, submodule)
        self._find_actions(subparsers, self)

#        self._add_bash_completion_subparser(subparsers)

        return parser

    def _find_actions(self, subparsers, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            # I prefer to be hypen-separated instead of underscores.
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            help = desc.strip().split('\n')[0]
            arguments = getattr(callback, 'arguments', [])

            subparser = subparsers.add_parser(command,
                                              help=help,
                                              description=desc,
                                              add_help=False,
                                              formatter_class=HelpFormatter
                                              )
            subparser.add_argument('-h', '--help',
                                   action='help',
                                   help=argparse.SUPPRESS,
                                   )
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    def _get_client_url(self, args):
        """Translate the available url-related options into a single string.

        Return the endpoint that should be used to talk to client if a
        clear decision can be made. Otherwise, return None.
        """
        if args.os_nal_url:
            return args.os_nal_url
        else:
            return None

    def _get_endpoint(self, args, force_auth=False):
        client_url = self._get_client_url(args)

        auth_reqd = force_auth or (utils.is_authentication_required(args.func)
                                   and not client_url)

        if not auth_reqd:
            endpoint = client_url
        else:
            endpoint = ''

        return endpoint

    def _get_versioned_client(self, api_version, args, force_auth=False):
        endpoint = self._get_endpoint(args, force_auth=force_auth)

        kwargs = {'id_pass': args.id_password}

        cl = client.Client(api_version, endpoint, **kwargs)
        return cl

    def main(self, argv):
        # Parse args once to find version

        # NOTE(flepied) Under Python3, parsed arguments are removed
        # from the list so make a copy for the first parsing
        base_argv = copy.deepcopy(argv)
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(base_argv)

        try:
            endpoint = self._get_client_url(options)
            endpoint, url_version = utils.strip_version(endpoint)
        except ValueError:
            url_version = None

        # build available subcommands based on version
        try:
            api_version = int(url_version or 1)
        except ValueError:
            print("Invalid API version parameter")
            utils.exit()

        subcommand_parser = self.get_subcommand_parser(api_version)
        self.parser = subcommand_parser

        # Handle top-level --help/-h before attempting to parse
        # a command off the command line
        if options.help or not argv:
            self.do_help(options)
            return 0

        # Parse args again and call whatever callback was selected
        args = subcommand_parser.parse_args(argv)

        # Short-circuit and deal with help command right away.
        if args.func == self.do_help:
            self.do_help(args)
            return 0

        LOG = logging.getLogger(client_const.SHELL_LOGGER_NAME)
        LOG.addHandler(logging.StreamHandler())
        LOG.setLevel(logging.DEBUG if args.debug else logging.INFO)

        client = self._get_versioned_client(api_version, args,
                                            force_auth=False)

        try:
            args.func(client, args)
        except Exception:
            # NOTE(kragniz) Print any exceptions raised to stderr
            # if the --debug flag is set
            if args.debug:
                traceback.print_exc()
            raise exc.CommandError("CommandError")

    @utils.arg('command', metavar='<subcommand>', nargs='?',
               help='Display help for <subcommand>.')
    def do_help(self, args):
        """Display help about this program or one of its subcommands.
        """
        if getattr(args, 'command', None):
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise exc.CommandError("'%s' is not a valid subcommand" %
                                       args.command)
        else:
            self.parser.print_help()


class HelpFormatter(argparse.HelpFormatter):

    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(HelpFormatter, self).start_section(heading)


def main():
    try:
        NalClientShell().main(sys.argv[1:])
    except KeyboardInterrupt:
        utils.exit('... terminating client', exit_code=130)
    except Exception as e:
        utils.exit(utils.exception_to_str(e))
