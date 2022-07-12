import json
import os

class ManoProtocolsVersion():

    MANO_PROTOCOL_BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/mano-proto'
    MANO_PROTO_RESOURCE_PATH = "resources"
    MANO_PROTO_FILENAME = "mano-versions.json" 

    def get_fragment_versions(self, protocol, protocol_version, fragment):
        mano_version_file     = self.MANO_PROTOCOL_BASE_DIR + "/" + protocol_version + "/" + self.MANO_PROTO_RESOURCE_PATH + "/" + protocol_version + "/" + self.MANO_PROTO_FILENAME
        data = dict()        
        with open(mano_version_file) as f:
            data = json.load(f)
            
        #loop in the protocal object list.
        for d in data:
            #
            _version  = d.get('version')
            _protocol = d.get('protocol')
            
            if _protocol == protocol and _version == protocol_version:
                fragment_list = d.get('protocols')
                for fragment_obj in fragment_list:
                    frag = fragment_obj.get('fragment')
                    header_v = fragment_obj.get('version')
                    
                    if frag == fragment:
                        frag_v = header_v[:1]
                        return {'fragment_version': frag_v,'header_version': header_v}
        return {}
