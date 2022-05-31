import json
import uuid
import os
import errno
import sys
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('nsd_name', var_type='String')
context = Variables.task_call(dev_var)

#filename is created based-on the device external reference
uuid_gen = str(uuid.uuid4())
if 'uuid_gen' in context:
    uuid_gen = context.get('uuid_gen')

nsd_name = ''
if not 'nsd_name_uuid' in context:
    # if the uuid_gen exists in the context do not create a new one. This allow to update the existing NSD.
    nsd_name = ''
    name = context.get('nsd_name')
    if name:
        nsd_name = name + '_' + uuid_gen

    #Store vnfd_name_uuid in context.
    context.update(nsd_name_uuid=nsd_name)
else:
    nsd_name = context.get('nsd_name_uuid')

nsd_sol0001_schema = 'etsi_nfv_sol001_nsd_types.yaml'
filename = '/opt/fmc_repository/Datafiles/NFV/NSD/' + nsd_name + '/Definitions/' + nsd_sol0001_schema

#nsd_sol0001_schema content

etsi_nfv_sol001_nsd_types = """
tosca_definitions_version: tosca_simple_yaml_1_3
description: ETSI NFV SOL 001 nsd types definitions version 3.5.1
metadata:
  template_name: etsi_nfv_sol001_nsd_types
  template_author: ETSI_NFV
  template_version: 3.5.1

imports:
     - https://forge.etsi.org/rep/nfv/SOL001/raw/v3.5.1/etsi_nfv_sol001_common_types.yaml
     - https://forge.etsi.org/rep/nfv/SOL001/raw/v3.5.1/etsi_nfv_sol001_vnfd_types.yaml
     - https://forge.etsi.org/rep/nfv/SOL001/raw/v3.5.1/etsi_nfv_sol001_pnfd_types.yaml
# editor's note: During the development of the SOL001ed351 GS, to enable this file to be verified by a TOSCA parser, the imports statement has to be replaced with a reference to a local copy of the common definitions YAML file

data_types:
  tosca.datatypes.nfv.NsVlProfile:
    derived_from: tosca.datatypes.Root
    description: Describes additional instantiation data for a given NsVirtualLink used in a specific NS deployment flavour.
    properties:
      max_bitrate_requirements:
        type: tosca.datatypes.nfv.LinkBitrateRequirements
        description: Specifies the maximum bitrate requirements for a VL instantiated according to this profile.
        required: true
      min_bitrate_requirements:
        type: tosca.datatypes.nfv.LinkBitrateRequirements
        description: Specifies the minimum bitrate requirements for a VL instantiated according to this profile.
        required: true
      qos:
        type: tosca.datatypes.nfv.NsVirtualLinkQos
        description: Specifies the QoS requirements of a VL instantiated according to this profile.
        required: false
      service_availability_level:
        type: integer
        description: Specifies the service availability level for the VL instance created from this profile
        required: false
        constraints:
          - greater_or_equal: 1
      virtual_link_protocol_data:
        type: list
        description: Specifies the protocol data for a virtual link.
        required: false
        entry_schema:
          type: tosca.datatypes.nfv.NsVirtualLinkProtocolData

  tosca.datatypes.nfv.NsVirtualLinkQos:
    derived_from: tosca.datatypes.nfv.Qos
    description: describes QoS data for a given VL used in a VNF deployment flavour
    properties:
      priority:
        type: integer
        constraints:
          - greater_or_equal: 0
        description: Specifies the priority level in case of congestion on the underlying physical links
        required: false

  tosca.datatypes.nfv.NsProfile:
    derived_from: tosca.datatypes.Root
    description: describes a profile for instantiating NSs of a particular NS DF according to a specific NSD and NS DF.
    properties:
      ns_instantiation_level:
        type: string
        description: Identifier of the instantiation level of the NS DF to be used for instantiation. If not present, the default instantiation level as declared in the NSD shall be used.
        required: false
      min_number_of_instances:
        type: integer
        description: Minimum number of instances of the NS based on this NSD that is permitted to exist for this NsProfile.
        required: true
        constraints:
          - greater_or_equal: 0
      max_number_of_instances:
        type: integer
        description: Maximum number of instances of the NS based on this NSD that is permitted to exist for this NsProfile.
        required: true
        constraints:
          - greater_or_equal: 0
      flavour_id:
        type: string
        description: Identifies the applicable network service DF within the scope of the NSD.
        required: true

  tosca.datatypes.nfv.Mask:
    derived_from: tosca.datatypes.Root
    properties:
      starting_point:
        description: Indicates the offset between the last bit of the source mac address and the first bit of the sequence of bits to be matched.
        type: integer
        required: true
      length:
        description: Indicates the number of bits to be matched.
        type: integer
        required: true
      value:
        description: Provide the sequence of bit values to be matched.
        type: string
        required: true

  tosca.datatypes.nfv.NsOperationAdditionalParameters:
    derived_from: tosca.datatypes.Root
    description: Is an empty base type for deriving data types for describing NS-specific additional parameters to be passed when invoking NS lifecycle management operations
    #properties:

  tosca.datatypes.nfv.NsMonitoringParameter:
    derived_from: tosca.datatypes.Root
    description: Represents information on virtualised resource related performance metrics applicable to the NS.
    properties:
      name:
        type: string
        description: Human readable name of the monitoring parameter
        required: true
      performance_metric:
        type: string
        description: Identifies a performance metric to be monitored, according to ETSI GS NFV-IFA 027.
        required: true
        constraints:
           - valid_values: [byte_incoming_sap, byte_outgoing_sap, packet_incoming_sap, packet_outgoing_sap, byte_incoming, byte_outgoing, packet_incoming, packet_outgoing ]
      collection_period:
        type: scalar-unit.time
        description: Describes the periodicity at which to collect the performance information.
        required: false

  tosca.datatypes.nfv.NsVirtualLinkProtocolData:
    derived_from: tosca.datatypes.Root
    description: describes one protocol layer and associated protocol data for a given virtual link used in a specific NS deployment flavour
    properties:
      associated_layer_protocol:
         type: string
         description: Identifies one of the protocols a virtualLink gives access to (ethernet, mpls, odu2, ipv4, ipv6, pseudo-wire) as specified by the connectivity_type property.
         required: true
         constraints:
           - valid_values: [ ethernet, mpls, odu2, ipv4, ipv6, pseudo-wire ]
      l2_protocol_data:
         type: tosca.datatypes.nfv.NsL2ProtocolData
         description: Specifies the L2 protocol data for a virtual link. Shall be present when the associatedLayerProtocol attribute indicates a L2 protocol and shall be absent otherwise.
         required: false
      l3_protocol_data:
         type: tosca.datatypes.nfv.NsL3ProtocolData
         description: Specifies the L3 protocol data for this virtual link. Shall be present when the associatedLayerProtocol attribute indicates a L3 protocol and shall be absent otherwise.
         required: false

  tosca.datatypes.nfv.NsL2ProtocolData:
    derived_from: tosca.datatypes.Root
    description: describes L2 protocol data for a given virtual link used in a specific NS deployment flavour.
    properties:
      name:
        type: string
        description: Identifies the network name associated with this L2 protocol.
        required: false
      network_type:
        type: string
        description: Specifies the network type for this L2 protocol. The value may be overridden at run-time.
        required: false
        constraints:
          - valid_values: [ flat, vlan, vxlan, gre ]
      vlan_transparent:
        type: boolean
        description: Specifies whether to support VLAN transparency for this L2 protocol or not.
        required: false
        default: false
      mtu:
        type: integer
        description: Specifies the maximum transmission unit (MTU) value for this L2 protocol.
        required: false
        constraints:
          - greater_than: 0
      segmentation_id:
        type: string
        description: Specifies a specific virtualised network segment, which depends on the network type. For e.g., VLAN ID for VLAN network type and tunnel ID for GRE/VXLAN network types
        required: false

  tosca.datatypes.nfv.NsL3ProtocolData:
    derived_from: tosca.datatypes.Root
    description: describes L3 protocol data for a given virtual link used in a specific NS deployment flavour.
    properties:
      name:
        type: string
        description: Identifies the network name associated with this L3 protocol.
        required: false
      ip_version:
        type: string
        description: Specifies IP version of this L3 protocol. The value of the ip_version property shall be consistent with the value of the layer_protocol in the connectivity_type property of the virtual link node.
        required: true
        constraints:
          - valid_values: [ ipv4, ipv6 ]
      cidr:
        type: string
        description: Specifies the CIDR (Classless Inter-Domain Routing) of this L3 protocol. The value may be overridden at run-time.
        required: true
      ip_allocation_pools:
        type: list
        description: Specifies the allocation pools with start and end IP addresses for this L3 protocol. The value may be overridden at run-time.
        required: false
        entry_schema:
          type: tosca.datatypes.nfv.NsIpAllocationPool

  tosca.datatypes.nfv.NsIpAllocationPool:
    derived_from: tosca.datatypes.Root
    description: Specifies a range of IP addresses
    properties:
      start_ip_address:
        type: string
        description: The IP address to be used as the first one in a pool of addresses derived from the cidr block full IP range
        required: true
      end_ip_address:
        type: string
        description: The IP address to be used as the last one in a pool of addresses derived from the cidr block full IP range
        required: true

  tosca.datatypes.nfv.NsScalingAspect:
    derived_from: tosca.datatypes.Root
    description: describes the details of an aspect used for horizontal scaling
    properties:
      name:
        type: string
        description: Human readable name of the aspect
        required: true
      description:
        type: string
        description: Human readable description of the aspect
        required: true
      ns_scale_levels:
        type: map
        description: Description of the NS levels for this scaling aspect.
        required: true
        key_schema:
          type: integer # Integer type in order to number the levels. First level is level 0.
        entry_schema:
          type: tosca.datatypes.nfv.NsLevels

  tosca.datatypes.nfv.NsLevels:
    derived_from: tosca.datatypes.Root
    description: describes the Ns levels
    properties:
      description:
        type: string
        description: Human readable description of the Ns level
        required: true

  tosca.datatypes.nfv.scaleNsByStepsData:
    derived_from: tosca.datatypes.Root
    description: describes the information needed to scale an NS instance by one or more scaling steps, with respect to a particular NS scaling aspect
    properties:
      scaling_direction:
        type: string
        description: Indicates the type of the scale operation requested.
        required: true
        constraints:
          - valid_values: [ scale_out, scale_in ]
      aspect:
        type: string
        description: Identifier of the scaling aspect.
        required: true
      number_of_steps:
        type: integer
        description: Number of scaling steps to be executed.
        required: true
        constraints:
          - greater_than: 0
        default: 1

  tosca.datatypes.nfv.scaleNsToLevelData:
    derived_from: tosca.datatypes.Root
    description: describes the information needed to scale an NS instance to a target size.
    properties:
      instantiation_level:
        type: string
        description: Identifier of the target instantiation level of the current deployment flavour to which the NS is requested to be scaled. Either instantiation_level or ns_scale_info shall be provided.
        required: false
      ns_scale_info:
        type: map # key: aspectId
        description: For each scaling aspect of the current deployment flavour, indicates the target scale level to which the NS is to be scaled. Either instantiation_level or ns_scale_info shall be provided.
        required: false
        entry_schema:
          type: integer

capability_types:
  tosca.capabilities.nfv.Forwarding:
    derived_from: tosca.capabilities.Root

relationship_types:
  tosca.relationships.nfv.ForwardTo:
    derived_from: tosca.relationships.Root
    valid_target_types: [ tosca.capabilities.nfv.Forwarding ]

interface_types:
  tosca.interfaces.nfv.Nslcm:
    derived_from: tosca.interfaces.Root
    description: This interface encompasses a set of TOSCA operations corresponding to NS LCM operations defined in ETSI GS NFV-IFA 013. as well as to preamble and postamble procedures to the execution of the NS LCM operations.
    operations:
      instantiate_start:
        description: Preamble to execution of the instantiate operation
      instantiate:
        description: Base procedure for instantiating an NS, corresponding to the Instantiate NS operation defined in ETSI GS NFV-IFA 013.
        # inputs:
          # additional_parameters:
          #   type: tosca.datatypes.nfv.NsOperationAdditionalParameters
          #   required: false
      instantiate_end:
        description: Postamble to the execution of the instantiate operation
      terminate_start:
        description: Preamble to execution of the terminate operation
      terminate:
        description: Base procedure for terminating an NS, corresponding to the Terminate NS operation defined in ETSI GS NFV-IFA 013.
      terminate_end:
        description: Postamble to the execution of the terminate operation
      update_start:
        description: Preamble to execution of the update operation
      update:
        description: Base procedure for updating an NS, corresponding to the Update NS operation defined in ETSI GS NFV-IFA 013.
      update_end:
        description: Postamble to the execution of the update operation
      scale_start:
        description: Preamble to execution of the scale operation
      scale:
        description: Base procedure for scaling an NS, corresponding to the Scale NS operation defined in ETSI GS NFV-IFA 013.
        # inputs:
          # additional_parameters:
          #   type: tosca.datatypes.nfv.NsOperationAdditionalParameters
          #   required: false
        inputs:
          scale_ns_by_steps_data:
            type: tosca.datatypes.nfv.scaleNsByStepsData
            description: Describes the information needed to scale an NS instance by one or more scaling steps, with respect to a particular NS scaling aspect as defined in ETSI GS NFV-IFA 013. Either scale_ns_by_steps_data or scale_ns_to_level_data shall be provided.
            required: false
          scale_ns_to_level_data:
            type: tosca.datatypes.nfv.scaleNsToLevelData
            description: Describes the information needed to scale an NS instance to a target size as defined in ETSI GS NFV-IFA 013. Either scale_ns_by_steps_data or scale_ns_to_level_data shall be provided.
            required: false
      scale_end:
        description: Postamble to the execution of the scale operation
      heal_start:
        description: Preamble to execution of the heal operation
      heal:
        description: Base procedure for healing an NS, corresponding to the Heal NS operation defined in ETSI GS NFV-IFA 013.
        # inputs:
          # additional_parameters:
          #   type: tosca.datatypes.nfv.NsOperationAdditionalParameters
          #   required: false
      heal_end:
        description: Postamble to the execution of the heal operation

  tosca.interfaces.nfv.NsVnfIndicator:
    derived_from: tosca.interfaces.Root
    description: This interface is an empty base interface type for deriving NS specific interface types that include VNF indicator specific notifications which will be used in a NS.

node_types:
  tosca.nodes.nfv.NS:
    derived_from: tosca.nodes.Root
    properties:
      descriptor_id:
        type: string # UUID
        description: Identifier of this NS descriptor
        required: true
      designer:
        type: string
        description: Identifies the designer of the NSD.
        required: true
      version:
        type: string
        description: Identifies the version of the NSD.
        required: true
      name:
        type: string
        description: Provides the human readable name of the NSD.
        required: true
      invariant_id: # UUID
        type: string
        description: Identifies an NSD in a version independent manner. This attribute is invariant across versions of NSD
        required: true
      flavour_id:
        type: string
        description: Identifier of the NS Deployment Flavour within the NSD
        required: true
      ns_profile:
        type: tosca.datatypes.nfv.NsProfile
        description: Specifies a profile of a NS, when this NS is used as nested NS within another NS.
        required: false
      service_availability_level:
        type: integer
        description: Specifies the service availability level for the NS instance.
        required: false
        constraints:
          - greater_or_equal: 1
      priority:
        type: integer
        description: Specifies the priority for the NS instance. Examples for the usage of priority include conflict resolution in case of resource shortage.
        required: false
        constraints:
          - greater_or_equal: 0
    attributes:
      scale_status:
        type: map # key: aspectId
        description: Scale status of the NS, one entry per aspect. Represents for every scaling aspect how "big" the NS has been scaled w.r.t. that aspect.
        entry_schema:
          type: integer
    requirements:
      - virtual_link:
          capability: tosca.capabilities.nfv.VirtualLinkable
          relationship: tosca.relationships.nfv.VirtualLinksTo
          node: tosca.nodes.nfv.NsVirtualLink
          occurrences: [ 0, 1 ]
    interfaces:
      Nslcm:
        type: tosca.interfaces.nfv.Nslcm

  tosca.nodes.nfv.Sap:
    derived_from: tosca.nodes.nfv.Cp
    description: node definition of SAP.
    requirements:
      - external_virtual_link:
          capability: tosca.capabilities.nfv.VirtualLinkable
          relationship: tosca.relationships.nfv.VirtualLinksTo
          occurrences: [0, 1]
      - internal_virtual_link:
          capability: tosca.capabilities.nfv.VirtualLinkable
          relationship: tosca.relationships.nfv.VirtualLinksTo
          occurrences: [1, 1]

  tosca.nodes.nfv.NsVirtualLink:
    derived_from: tosca.nodes.Root
    description: node definition of Virtual Links
    properties:
      vl_profile:
        type: tosca.datatypes.nfv.NsVlProfile # only covers min/max bitrate requirements
        description: Specifies instantiation parameters for a virtual link of a particular NS deployment flavour.
        required: true
      connectivity_type:
        type: tosca.datatypes.nfv.ConnectivityType
        required: true
      test_access:
        type: list
        description: Test access facilities available on the VL
        required: false
        entry_schema:
          type: string
          constraints:
            - valid_values: [ passive_monitoring, active_loopback ]
      description:
        type: string
        required: false
        description: Human readable information on the purpose of the virtual link (e.g. VL for control plane traffic).
    capabilities:
      virtual_linkable:
        type: tosca.capabilities.nfv.VirtualLinkable

  tosca.nodes.nfv.NfpPositionElement:
    derived_from: tosca.nodes.Root
    description: node definition of NfpPositionElement
    capabilities:
      forwarding:
        type: tosca.capabilities.nfv.Forwarding
    requirements:
      - profile_element:
          capability: tosca.capabilities.nfv.Forwarding
          relationship: tosca.relationships.nfv.ForwardTo
          occurrences: [ 1, 2 ] # When the number of occurrences is 1, the ingress and egress traffic is associated to a single VnfExtCp or Sap; When the number of occurrences is 2, the ingress VnfExtCp or Sap is associated to the first value and the egress VnfExtCp or Sap is associated to the second value.

  tosca.nodes.nfv.NfpPosition:
    derived_from: tosca.nodes.Root
    description: node definition of NFP position
    properties:
      forwarding_behaviour:
        type: string
        description: Identifies a rule to apply to forward traffic to CP or SAP instances corresponding to the referenced NfpPositionElement(s).
        constraints:
          - valid_values: [ all, lb, ff ]
        required: false
#     forwarding_behaviour_input_parameters:
#       description: Provides input parameters to configure the forwarding behaviour.
#       type: map
#       required: false
#       entry_schema:
#         type: strin
    capabilities:
      forwarding:
        type: tosca.capabilities.nfv.Forwarding
    requirements:
      - element:
          capability: tosca.capabilities.nfv.Forwarding
          node: tosca.nodes.nfv.NfpPositionElement
          relationship: tosca.relationships.nfv.ForwardTo
          occurrences: [ 1, UNBOUNDED ]

  tosca.nodes.nfv.NFP:
    derived_from: tosca.nodes.Root
    description: node definition of NFP
    requirements:
      - nfp_position:
          capability: tosca.capabilities.nfv.Forwarding
          node: tosca.nodes.nfv.NfpPosition
          relationship: tosca.relationships.nfv.ForwardTo
          occurrences: [ 1, UNBOUNDED ]

  tosca.nodes.nfv.Forwarding:
    derived_from: tosca.nodes.Root
    capabilities:
      virtual_linkable:
        type: tosca.capabilities.nfv.VirtualLinkable
      forwarding:
        type: tosca.capabilities.nfv.Forwarding
        occurrences: [ 1, 2 ]  #When the number of occurrences is 1, the ingress and egress traffic is associated to a single VnfExtCp, PnfExtCp or Sap; When the number of occurrences is 2, the ingress VnfExtCp, PnfExtCp or Sap is associated to the first value and the egress VnfExtCp, PnfExtCp or Sap is associated to the second value.
    requirements:
      - virtual_link:
          capability: tosca.capabilities.nfv.VirtualLinkable
          relationship: tosca.relationships.nfv.VirtualLinksTo

group_types:
  tosca.groups.nfv.NsPlacementGroup:
    derived_from: tosca.groups.Root
    description: NsPlacementGroup is used for describing the affinity or anti-affinity relationship applicable between VNF instances created using different VNFDs, the Virtual Link instances created using different VLDs or the nested NS instances created using different NSDs when used in a NSD.
    properties:
      description:
        type: string
        description: Human readable description of the group
        required: true
    members: [tosca.nodes.nfv.VNF, tosca.nodes.nfv.NsVirtualLink, tosca.nodes.nfv.NS]

  tosca.groups.nfv.VNFFG:
    derived_from: tosca.groups.Root
    description: the VNFFG group type describes a topology of the NS or a portion of the NS, and optionally forwarding rules, applicable to the traffic conveyed over this topology
    properties:
      description:
        type: string
        description: Human readable description of the group
        required: true
    members: [ tosca.nodes.nfv.NFP, tosca.nodes.nfv.VNF, tosca.nodes.nfv.PNF, tosca.nodes.nfv.NS, tosca.nodes.nfv.NsVirtualLink, tosca.nodes.nfv.NfpPositionElement ]


policy_types:
  tosca.policies.nfv.NsAffinityRule:
    derived_from: tosca.policies.Placement
    description: The NsAffinityRule describes the affinity rules applicable for the defined targets
    properties:
      scope:
        type: string
        description: Specifies the scope of the local affinity rule.
        required: true
        constraints:
          - valid_values: [ nfvi_node, zone, zone_group, nfvi_pop, network_link_and_node ]
    targets: [tosca.nodes.nfv.VNF, tosca.nodes.nfv.NsVirtualLink, tosca.nodes.nfv.NS, tosca.groups.nfv.NsPlacementGroup ]

  tosca.policies.nfv.NsAntiAffinityRule:
    derived_from: tosca.policies.Placement
    description: The NsAntiAffinityRule describes the anti-affinity rules applicable for the defined targets
    properties:
      scope:
        type: string
        description: Specifies the scope of the local affinity rule..
        required: true
        constraints:
          - valid_values: [ nfvi_node, zone, zone_group, nfvi_pop, network_link_and_node ]
    targets: [tosca.nodes.nfv.VNF, tosca.nodes.nfv.NsVirtualLink, tosca.nodes.nfv.NS, tosca.groups.nfv.NsPlacementGroup ]

  tosca.policies.nfv.NsSecurityGroupRule:
    derived_from: tosca.policies.nfv.Abstract.SecurityGroupRule
    description: The NsSecurityGroupRule type is a policy type specified the matching criteria for the ingress and/or egress traffic to/from visited SAPs.
    targets: [ tosca.nodes.nfv.Sap ]

  tosca.policies.nfv.NfpRule:
    derived_from: tosca.policies.Root
    description: policy definition of NfpRule
    properties:
      ether_destination_address:
        description: Indicates a destination Mac address.
        type: string
        required: false
      ether_source_address:
        description: Indicates a source Mac address.
        type: string
        required: false
      ether_type:
        description: Indicates the protocol carried over the Ethernet layer.
        type: string
        constraints:
          - valid_values: [ ipv4, ipv6 ]
        required: false
      vlan_tag:
        description: Indicates a VLAN identifier in an IEEE 802.1Q-2014 tag [14]. Multiple tags can be included for QinQ stacking.
        type: list
        entry_schema:
          type: string
        required: false
      protocol:
        description: 'Indicates the L4 protocol, For IPv4 [15] this corresponds to the field called "Protocol" to identify the next level protocol. For IPv6 [16] this corresponds to the field is called the "Next Header" field. Permitted values: Any keyword defined in the IANA [17] protocol registry.'
        type: string
        required: false
      dscp:
        description: For IPv4 [15] a string of "0" and "1" digits that corresponds to the 6-bit Differentiated Services Code Point (DSCP) field of the IP header. For IPv6 [16] a string of "0" and "1" digits that corresponds to the 6 differentiated services bits of the traffic class header field.
        type: string
        required: false
      source_port_range:
        description: Indicates a range of source ports.
        type: range
        required: false
        constraints:
          - in_range: [0, 65535]
      destination_port_range:
        description: Indicates a range of destination ports.
        type: range
        required: false
        constraints:
          - in_range: [0, 65535]
      source_ip_address_prefix:
        description: Indicates the source IP address range in CIDR format.
        type: string
        required: false
      destination_ip_address_prefix:
        description: Indicates the destination IP address range in CIDR format.
        type: string
        required: false
      extended_criteria:
        description: Indicates values of specific bits in a frame.
        type: list
        entry_schema:
          type: tosca.datatypes.nfv.Mask
        required: false
    targets: [ tosca.nodes.nfv.NFP ]

  tosca.policies.nfv.NsMonitoring:
    derived_from: tosca.policies.Root
    description: Policy type is used to identify information to be monitored during the lifetime of a network service instance as defined in ETSI GS NFV-IFA 014 [2].
    properties:
      ns_monitoring_parameters:
        type: map #key: id
        description: Specifies a virtualised resource related performance metric to be monitored on the NS level.
        required: true
        entry_schema:
          type: tosca.datatypes.nfv.NsMonitoringParameter
        constraints:
          - min_length: 1
    targets: [ tosca.nodes.nfv.NS ]

  tosca.policies.nfv.VnfMonitoring:
    derived_from: tosca.policies.Root
    description: Policy type is used to identify information to be monitored during the lifetime of a VNF instance as defined in ETSI GS NFV-IFA 014 [2].
    properties:
      vnf_monitoring_parameters:
        type: map #key: id
        description: Specifies a virtualised resource related performance metric to be monitored on the NS level.
        required: true
        entry_schema:
          type: tosca.datatypes.nfv.VnfMonitoringParameter
        constraints:
          - min_length: 1
    targets: [ tosca.nodes.nfv.VNF ]

  tosca.policies.nfv.NsScalingAspects:
    derived_from: tosca.policies.Root
    description: The ScalingAspects type is a policy type representing the scaling aspects used for horizontal scaling as defined in ETSI GS NFV-IFA 014 [2]
    properties:
      aspects:
        type: map # key: aspectId
        description: Describe the details of a particular aspect including the corresponding NS levels.
        required: true
        entry_schema:
          type: tosca.datatypes.nfv.NsScalingAspect
        constraints:
          - min_length: 1

  tosca.policies.nfv.VnfToLevelMapping:
    derived_from: tosca.policies.Root
    description: The VnfToLevelMapping type is a policy type representing the number of VNF instances to be deployed at each NS level, as defined in ETSI GS NFV-IFA 014 [2]
    properties:
      aspect:
        type: string
        description: Represents the scaling aspect to which this policy applies
        required: true
      number_of_instances:
        type: map # key: Ns level
        description: Number of VNF instances to be deployed for each NS level.
        required: true
        key_schema:
          type: integer # First level is level 0.
        entry_schema:
          type: integer
        constraints:
          - min_length: 1
    targets: [ tosca.nodes.nfv.VNF ]

  tosca.policies.nfv.NsToLevelMapping:
    derived_from: tosca.policies.Root
    description: The NsToLevelMapping type is a policy type representing the number of NS instances of a nested NS to be deployed at each NS level of the composite NS, as defined in ETSI GS NFV-IFA 014 [2]
    properties:
      aspect:
        type: string
        description: Represents the scaling aspect to which this policy applies
        required: true
      number_of_instances:
        type: map # key: Ns level
        description: Number of NS instances of a nested NS to be deployed for each NS level of the composite NS.
        required: true
        key_schema:
          type: integer # First level is level 0.
        entry_schema:
          type: integer
        constraints:
          - min_length: 1
    targets: [ tosca.nodes.nfv.NS ]

  tosca.policies.nfv.VirtualLinkToLevelMapping:
    derived_from: tosca.policies.Root
    description: The VirtualLinkToLevelMapping type is a policy type representing the number of NS instances of a nested NS to be deployed at each NS level of the composite NS, as defined in ETSI GS NFV-IFA 014 [2]
    properties:
      aspect:
        type: string
        description: Represents the scaling aspect to which this policy applies
        required: true
      bit_rate_requirements:
        type: map # key: Ns level
        description: Bitrate requirements of a VL for each NS level.
        required: true
        key_schema:
          type: integer # First level is level 0.
        entry_schema:
          type: tosca.datatypes.nfv.LinkBitrateRequirements
        constraints:
          - min_length: 1
    targets: [ tosca.nodes.nfv.NsVirtualLink ]

  tosca.policies.nfv.NsInstantiationLevels:
    derived_from: tosca.policies.Root
    description: The NsInstantiationLevels type is a policy type representing all the instantiation levels of resources to be instantiated within a deployment flavour and including default instantiation level in term of the number of VNF and nested NS instances to be created as defined in ETSI GS NFV-IFA 014 [2].
    properties:
      ns_levels:
        type: map # key: levelId
        description: Describes the various levels of resources that can be used to instantiate the VNF using this flavour.
        required: true
        entry_schema:
          type: tosca.datatypes.nfv.NsLevels
        constraints:
          - min_length: 1
      default_level:
        type: string # levelId
        description: The default instantiation level for this flavour.
        required: false # required if multiple entries in ns_levels

  tosca.policies.nfv.VnfToInstantiationLevelMapping:
    derived_from: tosca.policies.Root
    description: The VnfToInstantiationLevelMapping type is a policy type representing the number of VNF instances to be deployed at each NS instantiation level, as defined in ETSI GS NFV-IFA 014 [2]
    properties:
      number_of_instances:
        type: map # key: Ns instantiation level
        description: Number of VNF instances to be deployed for each NS instantiation level.
        required: true
        entry_schema:
          type: integer
        constraints:
          - min_length: 1
    targets: [ tosca.nodes.nfv.VNF ]

  tosca.policies.nfv.NsToInstantiationLevelMapping:
    derived_from: tosca.policies.Root
    description: The NsToInstantiationLevelMapping type is a policy type representing the number of NS instances of a nested NS to be deployed at each NS instantiation level of the composite NS, as defined in ETSI GS NFV-IFA 014 [2]
    properties:
      number_of_instances:
        type: map # key: Ns instantiation level
        description: Number of NS instances of a nested NS to be deployed for each NS instantiation level of the composite NS.
        required: true
        entry_schema:
          type: integer
        constraints:
          - min_length: 1
    targets: [ tosca.nodes.nfv.NS ]

  tosca.policies.nfv.VirtualLinkToInstantiationLevelMapping:
    derived_from: tosca.policies.Root
    description: The VirtualLinkToInstantiationLevelMapping type is a policy type describing the bitrate requirements of a VL at each NS instantiation level of the composite NS, as defined in ETSI GS NFV-IFA 014 [2]
    properties:
      bit_rate_requirements:
        type: map # key: Ns instantiation level
        description: Bitrate requirements of a VL for each NS instantiation level.
        required: true
        entry_schema:
          type: tosca.datatypes.nfv.LinkBitrateRequirements
        constraints:
          - min_length: 1
    targets: [ tosca.nodes.nfv.NsVirtualLink ]

  tosca.policies.nfv.NsAutoScale:
    derived_from: tosca.policies.Root
    description: The NsAutoScale policy type is a base policy type for defining NS auto-scale specific policies as defined in ETSI GS NFV-IFA 014 [2].
    targets: [ tosca.nodes.nfv.NS ]
"""

#create file in http server directory.
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
    with open(filename, "w") as file:
        file.write(etsi_nfv_sol001_nsd_types)
        file.close()


MSA_API.task_success('NS Descriptor schema is created successfully.', context, True)