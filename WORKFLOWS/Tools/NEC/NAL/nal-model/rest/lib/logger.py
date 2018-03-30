import logging

from rest.conf import config
LOG_FILE = getattr(config, 'LOG_OUTPUT_PASS', {})
LOG_LEVEL = getattr(config, 'LOG_OUTPUT_LEVEL', {})


class LibLogger():

    def __init__(self, request_id='-', operation_id='-',
                 IaaS_tenant_id='-', nal_tenant_id='-'):

        request_id = request_id if request_id else '-'
        operation_id = operation_id if operation_id else '-'
        IaaS_tenant_id = IaaS_tenant_id if IaaS_tenant_id else '-'
        nal_tenant_id = nal_tenant_id if nal_tenant_id else '-'

        # TODO set requestID here.
        log_fmt = '%(asctime)s.%(msecs)03d %(levelname)s %(name)s ' + \
                  '[' + request_id + ' ' + operation_id + ' ' + \
                  IaaS_tenant_id + ' ' + nal_tenant_id + '] %(message)s'
        logging.basicConfig(format=log_fmt,
                            filename=LOG_FILE,
                            level=getattr(logging, LOG_LEVEL, 0),
                            datefmt='%Y-%m-%d %H:%M:%S')

    def log_debug(self, name, msg):
        LOG = logging.getLogger(name)
        LOG.debug(msg)

    def log_info(self, name, msg):
        LOG = logging.getLogger(name)
        LOG.info(msg)

    def log_warn(self, name, msg):
        LOG = logging.getLogger(name)
        LOG.warn(msg)

    def log_error(self, name, msg):
        LOG = logging.getLogger(name)
        LOG.error(msg)

    def log_fatal(self, name, msg):
        LOG = logging.getLogger(name)
        LOG.fatal(msg)
