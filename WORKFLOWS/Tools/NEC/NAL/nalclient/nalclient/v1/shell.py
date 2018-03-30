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


"""Commandline subcommand  Method from."""

from __future__ import print_function

import json
from pprint import pprint

from nalclient.common import utils

FILE_ENCODE = ('utf-8', 's-jis')


@utils.arg('--type', metavar='<Type>',
           help='type of create node.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the node to create.')
def do_node_create(c, args):
    """Create a new node you can access.
    In commandline, output node data.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call client.
    result = c.node.create(fields)

    # Show result.
    print(result.get('status', 'non-status'))

    return result


@utils.arg('--type', metavar='<Type>',
           help='type of update node.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the node to update.')
def do_node_update(c, args):
    """Update a node by operate port.
    In commandline, output status.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call client.
    result = c.node.update(fields)

    # Show result.
    print(result.get('status', 'non-status'))

    return result


@utils.arg('--type', metavar='<Type>',
           help='type of delete node.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the node to delete.')
def do_node_delete(c, args):
    """Delete a node you can access.
    In commandline, output status.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call client.
    result = c.node.delete(fields)

    # Show result.
    print(result.get('status', 'non-status'))

    return result


@utils.arg('--type', metavar='<Type>',
           help='type of get node.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the node to get.')
def do_node_get(c, args):
    """Get node data you can access.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call Client
    data_list = c.node.get(fields)

    # Show result.
    pprint(data_list)


@utils.arg('--type', metavar='<Type>',
           help='type of create service.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the service to create.')
def do_service_create(c, args):
    """Create a new service you can access.
    In commandline, output status.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call client.
    result = c.service.create(fields)

    # Show result.
    print(result.get('status', 'non-status'))

    return result


@utils.arg('--type', metavar='<Type>',
           help='type of update service.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the service to update.')
def do_service_update(c, args):
    """Update a new service you can access.
    In commandline, output status.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call client.
    result = c.service.update(fields)

    # Show result.
    print(result.get('status', 'non-status'))

    return result


@utils.arg('--type', metavar='<Type>',
           help='type of delete service.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the service to delete.')
def do_service_delete(c, args):
    """Delete a new service you can access.
    In commandline, output status.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call client.
    result = c.service.delete(fields)

    # Show result.
    print(result.get('status', 'non-status'))

    return result


@utils.arg('--type', metavar='<Type>',
           help='type of get service.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the service to get.')
def do_service_get(c, args):
    """Get a new service you can access.
    In commandline, output service data.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call Client
    data_list = c.service.get(fields)

    # Show result.
    pprint(data_list)


@utils.arg('--type', metavar='<Type>',
           help='type of create resource.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the resource to create.')
def do_resource_create(c, args):
    """Create a new resource you can access.
    In commandline, output status.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call client.
    result = c.resource.create(fields)

    # Show result.
    print(result.get('status', 'non-status'))

    return result


@utils.arg('--type', metavar='<Type>',
           help='type of update resource.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the resource to update.')
def do_resource_update(c, args):
    """Update a new resource you can access.
    In commandline, output status.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call client.
    result = c.resource.update(fields)

    # Show result.
    print(result.get('status', 'non-status'))

    return result


@utils.arg('--type', metavar='<Type>',
           help='type of delete resource.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the resource to delete.')
def do_resource_delete(c, args):
    """Delete a new resource you can access.
    In commandline, output status.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call client.
    result = c.resource.delete(fields)

    # Show result.
    print(result.get('status', 'non-status'))

    return result


@utils.arg('--type', metavar='<Type>',
           help='type of get resource.')
@utils.arg('--json-data', metavar='<JSON_DATA>',
           help='Json format data of the resource to get.')
def do_resource_get(c, args):
    """Get a new resource you can access.
    In commandline, output resource data.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if not hasattr(args, 'type') or not args.type:
        msg = "too few arguments: type is required."
        utils.exit(msg)
    if not hasattr(args, 'json_data') or not args.json_data:
        msg = "too few arguments: json_data is required."
        utils.exit(msg)

    try:
        fields = json.loads(args.json_data)
    except Exception:
        msg = "json format is incorrect."
        utils.exit(msg)

    fields['function_type'] = args.type

    # Call Client
    data_list = c.resource.get(fields)

    # Show result.
    pprint(data_list)
