# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


class Show(AAZCommand):
    """Get a virtual machine image.
    """

    _aaz_info = {
        "version": "2024-07-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/providers/microsoft.compute/locations/{}/publishers/{}/artifacttypes/vmimage/offers/{}/skus/{}/versions/{}", "2024-07-01"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.location = AAZResourceLocationArg(
            required=True,
            id_part="name",
        )
        _args_schema.offer = AAZStrArg(
            options=["-f", "--offer"],
            help="A valid image publisher offer.",
            required=True,
            id_part="child_name_3",
        )
        _args_schema.publisher = AAZStrArg(
            options=["-p", "--publisher"],
            help="A valid image publisher.",
            required=True,
            id_part="child_name_1",
        )
        _args_schema.sku = AAZStrArg(
            options=["-s", "--sku"],
            help="A valid image SKU.",
            required=True,
            id_part="child_name_4",
        )
        _args_schema.version = AAZStrArg(
            options=["--version"],
            help="A valid image SKU version.",
            required=True,
            id_part="child_name_5",
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.VirtualMachineImagesGet(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class VirtualMachineImagesGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/providers/Microsoft.Compute/locations/{location}/publishers/{publisherName}/artifacttypes/vmimage/offers/{offer}/skus/{skus}/versions/{version}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "location", self.ctx.args.location,
                    required=True,
                ),
                **self.serialize_url_param(
                    "offer", self.ctx.args.offer,
                    required=True,
                ),
                **self.serialize_url_param(
                    "publisherName", self.ctx.args.publisher,
                    required=True,
                ),
                **self.serialize_url_param(
                    "skus", self.ctx.args.sku,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "version", self.ctx.args.version,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2024-07-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.extended_location = AAZObjectType(
                serialized_name="extendedLocation",
            )
            _schema_on_200.id = AAZStrType()
            _schema_on_200.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _schema_on_200.tags = AAZDictType()

            extended_location = cls._schema_on_200.extended_location
            extended_location.name = AAZStrType()
            extended_location.type = AAZStrType()

            properties = cls._schema_on_200.properties
            properties.architecture = AAZStrType()
            properties.automatic_os_upgrade_properties = AAZObjectType(
                serialized_name="automaticOSUpgradeProperties",
            )
            properties.data_disk_images = AAZListType(
                serialized_name="dataDiskImages",
            )
            properties.disallowed = AAZObjectType()
            properties.features = AAZListType()
            properties.hyper_v_generation = AAZStrType(
                serialized_name="hyperVGeneration",
            )
            properties.image_deprecation_status = AAZObjectType(
                serialized_name="imageDeprecationStatus",
            )
            properties.os_disk_image = AAZObjectType(
                serialized_name="osDiskImage",
            )
            properties.plan = AAZObjectType()

            automatic_os_upgrade_properties = cls._schema_on_200.properties.automatic_os_upgrade_properties
            automatic_os_upgrade_properties.automatic_os_upgrade_supported = AAZBoolType(
                serialized_name="automaticOSUpgradeSupported",
                flags={"required": True},
            )

            data_disk_images = cls._schema_on_200.properties.data_disk_images
            data_disk_images.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.data_disk_images.Element
            _element.lun = AAZIntType(
                flags={"read_only": True},
            )

            disallowed = cls._schema_on_200.properties.disallowed
            disallowed.vm_disk_type = AAZStrType(
                serialized_name="vmDiskType",
            )

            features = cls._schema_on_200.properties.features
            features.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.features.Element
            _element.name = AAZStrType()
            _element.value = AAZStrType()

            image_deprecation_status = cls._schema_on_200.properties.image_deprecation_status
            image_deprecation_status.alternative_option = AAZObjectType(
                serialized_name="alternativeOption",
            )
            image_deprecation_status.image_state = AAZStrType(
                serialized_name="imageState",
            )
            image_deprecation_status.scheduled_deprecation_time = AAZStrType(
                serialized_name="scheduledDeprecationTime",
            )

            alternative_option = cls._schema_on_200.properties.image_deprecation_status.alternative_option
            alternative_option.type = AAZStrType()
            alternative_option.value = AAZStrType()

            os_disk_image = cls._schema_on_200.properties.os_disk_image
            os_disk_image.operating_system = AAZStrType(
                serialized_name="operatingSystem",
                flags={"required": True},
            )

            plan = cls._schema_on_200.properties.plan
            plan.name = AAZStrType(
                flags={"required": True},
            )
            plan.product = AAZStrType(
                flags={"required": True},
            )
            plan.publisher = AAZStrType(
                flags={"required": True},
            )

            tags = cls._schema_on_200.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


class _ShowHelper:
    """Helper class for Show"""


__all__ = ["Show"]
