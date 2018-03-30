# -*- coding: utf-8 -*-

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
import logging


class LibLogger():

    def __init__(self, job_config,
                                request_id='-',
                                operation_id='-',
                                IaaS_tenant_id='-',
                                nal_tenant_id='-'):

        self.log_pass_mask = job_config.LOG_PASSWORD_MASK
        log_fmt = '%(asctime)s.%(msecs)03d %(levelname)s %(name)s ' + \
                  '[' + request_id + '] %(message)s'
        logging.basicConfig(
                            format=log_fmt,
                            filename=job_config.LOG_OUTPUT_PASS,
                            level=getattr(logging, job_config.LOG_LEVEL, 0),
                            datefmt=job_config.LOG_DATETIME_FORMAT)

    def __mask_password(self, msg, passwords):
        for val in passwords:
            if len(val) > 0:
                msg = msg.replace(val, self.log_pass_mask)
        return msg

    def log_debug(self, logger, msg, passwords=[]):
        LOG = logging.getLogger(logger)
        msg = self.__mask_password(msg, passwords)
        LOG.debug(msg)

    def log_info(self, logger, msg, passwords=[]):
        LOG = logging.getLogger(logger)
        msg = self.__mask_password(msg, passwords)
        LOG.info(msg)

    def log_warn(self, logger, msg):
        LOG = logging.getLogger(logger)
        LOG.warn(msg)

    def log_error(self, logger, msg):
        LOG = logging.getLogger(logger)
        LOG.error(msg)

    def log_fatal(self, logger, msg):
        LOG = logging.getLogger(logger)
        LOG.fatal(msg)
