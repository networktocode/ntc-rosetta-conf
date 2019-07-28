from typing import Any, Dict, cast

from jetconf.data import BaseDatastore
from jetconf.helpers import JsonNodeT

from ntc_rosetta import get_driver

from yangson.instance import InstanceNode


def _fail(msg: str) -> JsonNodeT:
    return {"result": "ntc-rosetta-config:error", "error-msg": msg}


def _succeed(result: Dict[str, Any]) -> JsonNodeT:
    r = {"result": "ntc-rosetta-config:success"}
    r.update(result)
    return r


def remove_ntc_rosetta_conf_specific_data(data: Dict[str, Any]) -> JsonNodeT:
    # we need to remove this because they are not part of ntc-rosetta
    data.pop("ntc-rosetta-conf:device")


class OpHandlersContainer:
    def __init__(self, ds: BaseDatastore):
        self.ds = ds

    def _get_instance_node(
        self, path: str, running: bool, username: str = ""
    ) -> InstanceNode:
        if running:
            data = self.ds.get_data_root()
        else:
            data = self.ds.get_data_root_staging(username)
        irt = self.ds._dm.parse_resource_id(path)
        return data.goto(irt)

    def _get_platform(self, username: str) -> str:
        try:
            return cast(
                str,
                self._get_instance_node(
                    "/ntc-rosetta-conf:device/config/platform", True, username
                ).raw_value(),
            )
        except Exception:
            return ""

    def ping(self, input_args: JsonNodeT, username: str) -> JsonNodeT:
        return _succeed({})

    def translate(self, input_args: JsonNodeT, username: str) -> JsonNodeT:
        db = input_args["ntc-rosetta-conf:database"]
        if db == "candidate":
            data = self._get_instance_node("/", False, username).raw_value()
        elif db == "running":
            data = self._get_instance_node("/", True, username).raw_value()
        else:
            return _fail(f"don't know this database: '{db}'")
        replace = input_args.get("ntc-rosetta-conf:replace", False)

        platform = self._get_platform(username)
        if not platform:
            return _fail(f"you need to set the platform first")

        device_driver = get_driver(platform.split(":")[-1], "openconfig")
        processor = device_driver()

        remove_ntc_rosetta_conf_specific_data(data)

        native = processor.translate(candidate=data, replace=replace)
        return _succeed({"native": native})

    def merge(self, input_args: JsonNodeT, username: str) -> JsonNodeT:
        candidate = self._get_instance_node("/", False, username).raw_value()
        running = self._get_instance_node("/", True, username).raw_value()
        replace = input_args.get("ntc-rosetta-conf:replace", False)

        platform = self._get_platform(username)
        if not platform:
            return _fail(f"you need to set the platform first")

        device_driver = get_driver(platform.split(":")[-1], "openconfig")
        processor = device_driver()

        remove_ntc_rosetta_conf_specific_data(candidate)
        remove_ntc_rosetta_conf_specific_data(running)

        native = processor.merge(candidate=candidate, running=running, replace=replace)
        return _succeed({"native": native})

    def parse(self, input_args: JsonNodeT, username: str) -> JsonNodeT:
        validate = input_args.get("ntc-rosetta-conf:validate", True)
        native = input_args.get("ntc-rosetta-conf:native")
        if not native:
            return _fail(f"you need to set native data")

        platform = self._get_platform(username)
        if not platform:
            return _fail(f"you need to set the platform first")

        device_driver = get_driver(platform.split(":")[-1], "openconfig")
        processor = device_driver()

        native = processor.parse(native={"dev_conf": native}, validate=validate)
        native_raw = native.raw_value()

        models_to_propagate = ["ntc-rosetta-conf:device"]
        for m in models_to_propagate:
            irt = self.ds._dm.parse_resource_id(f"/{m}")
            data = self.ds._data.goto(irt)
            native_raw[m] = data.raw_value()

        self.ds._data = self.ds._dm.from_raw(native_raw)
        return _succeed({})


def register_op_handlers(ds: BaseDatastore) -> None:
    op_handlers_obj = OpHandlersContainer(ds)
    ds.handlers.op.register(op_handlers_obj.merge, "ntc-rosetta-conf:merge")
    ds.handlers.op.register(op_handlers_obj.parse, "ntc-rosetta-conf:parse")
    ds.handlers.op.register(op_handlers_obj.ping, "ntc-rosetta-conf:ping")
    ds.handlers.op.register(op_handlers_obj.translate, "ntc-rosetta-conf:translate")
