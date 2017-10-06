# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

tosca_definitions_version: tosca_simple_yaml_1_0

# compile this with "m4 vhss.m4 > vhss.yaml"

# include macros
include(macros.m4)

node_types:
    tosca.nodes.VHSSService:
        derived_from: tosca.nodes.Root
        description: >
            vHSS Service
        capabilities:
            xos_base_service_caps
        properties:
            xos_base_props
            xos_base_service_props

    tosca.nodes.VHSSTenant:
        derived_from: tosca.nodes.Root
        description: >
            A Tenant of the vHSS service
        properties:
            xos_base_tenant_props

    tosca.nodes.VHSSVendor:
        derived_from: tosca.nodes.Root
        description: >
            VHSS Vendor
        properties:
            xos_base_props
            name:
                type: string
                required: true

    tosca.relationships.VendorOfTenant:
           derived_from: tosca.relationships.Root
           valid_target_types: [ tosca.capabilities.xos.VHSSTenant ]

