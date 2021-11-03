"""SDK to Json."""
import collections
import inspect
import json
from inspect import signature

from msa_sdk import util
from msa_sdk.conf_profile import ConfProfile
from msa_sdk.customer import Customer
from msa_sdk.device import Device
from msa_sdk.lookup import Lookup
from msa_sdk.orchestration import Orchestration
from msa_sdk.order import Order
from msa_sdk.repository import Repository
from msa_sdk.variables import Variables

device = Device()
lookup = Lookup()
order = Order(1)
orchestration = Orchestration(1)
repository = Repository()
customer = Customer()
conf_profile = ConfProfile()
variable = Variables()

output_doc = collections.defaultdict(dict)  # type: dict


def get_members(cls_name, obj):
    """Extract members."""
    output_doc[cls_name] = {"methods": list()}
    for i in inspect.getmembers(obj, predicate=inspect.ismethod):
        if i[0].startswith('__init__'):
            output_doc[cls_name]["methods"].append(
                {
                    i[0]: {
                        "description": inspect.getdoc(i[1]),
                        "parameters": str(signature(i[1]))
                    }
                }
            )
        if not i[0].startswith('_'):
            output_doc[cls_name]["methods"].append(
                {
                    i[0]: {
                        "description": inspect.getdoc(i[1]),
                        "parameters": str(signature(i[1]))
                    }
                }
            )


def get_members_function():
    """Exctract members of a function."""
    output_doc["util"] = {"methods": list()}
    for func_name, funcobj in inspect.getmembers(util,
                                                 predicate=inspect.isfunction):
        output_doc["util"]["methods"].append(
            {
                func_name: {
                    "description": inspect.getdoc(funcobj),
                    "parameters": str(signature(funcobj))
                }
            }
        )


get_members('Device', device)
get_members('Lookup', lookup)
get_members('Order', order)
get_members('Repository', repository)
get_members('Customer', customer)
get_members('ConfProfile', conf_profile)
get_members('Variables', variable)

get_members_function()


print(json.dumps(output_doc))