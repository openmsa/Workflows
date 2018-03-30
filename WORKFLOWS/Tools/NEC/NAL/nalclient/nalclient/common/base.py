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



# TODO(aababilov): call run_hooks() in HookableMixin's child classes
class HookableMixin(object):
    """Mixin so classes can register and run hooks."""
    _hooks_map = {}


class BaseManager(HookableMixin):
    """Basic manager type providing common operations.

    Managers interact with a particular type of API (servers, flavors, tickets,
    etc.) and provide CRUD operations for them.
    """
    resource_class = None

    def __init__(self, client):
        """Initializes BaseManager with `client`.

        :param client: instance of BaseClient descendant for HTTP requests
        """
        super(BaseManager, self).__init__()
        self.client = client
