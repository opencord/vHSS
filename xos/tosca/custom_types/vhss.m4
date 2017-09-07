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
        capabilities:
            xos_bas_service_caps
        properties:
            name:
                type: string
                required: true

    tosca.relationships.VendorOfTenant:
           derived_from: tosca.relationships.Root
           valid_target_types: [ tosca.capabilities.xos.VHSSTenant ]

