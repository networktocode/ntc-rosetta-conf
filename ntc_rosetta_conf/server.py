import json
import logging
import pathlib
import sys
import tempfile
import uuid
from typing import cast


import colorlog
from colorlog import error, info

from jetconf import config, jetconf, op_internal
from jetconf.errors import JetconfInitError
from jetconf.helpers import ErrorHelpers
from jetconf.rest_server import RestServer

from ntc_rosetta import yang as ntc_rosetta_yang

import ntc_rosetta_conf

from yangson.datamodel import DataModel
from yangson.enumerations import ContentType, ValidationScope
from yangson.exceptions import YangsonException
from yangson.schemanode import SchemaError, SemanticError


def get_data_model(model_name: str) -> DataModel:
    lib = ntc_rosetta_yang.OPENCONFIG_LIB
    path = ntc_rosetta_yang.OPENCONFIG_PATH
    with open(lib, "r") as f:
        lib_data = json.load(f)

    extra_modules = [
        {
            "name": "ietf-yang-library",
            "revision": "2016-06-21",
            "conformance-type": "implement",
        },
        {
            "name": "ntc-rosetta-conf",
            "revision": "2019-06-26",
            "conformance-type": "implement",
        },
    ]
    lib_data["ietf-yang-library:modules-state"]["module"].extend(extra_modules)
    path.append(pathlib.Path(__file__).parent.joinpath("yang"))

    tmp_file = pathlib.Path(tempfile.gettempdir()).joinpath(str(uuid.uuid4()))
    with open(tmp_file, "w") as f:
        json.dump(lib_data, f)
    return DataModel.from_file(tmp_file, path)


class RosettaconfConfig(config.JcConfig):
    def __init__(
        self,
        log_level: str,
        data_file: str,
        pid_file: str,
        listen_on_localhost_only: bool,
        port: int,
        ssl_crt: str,
        ssl_key: str,
        ca_crt: str,
        disable_ssl: bool,
    ) -> None:
        yang_mod_dir_env = "asda"

        glob_def = {
            "TIMEZONE": "GMT",
            "LOGFILE": "-",
            "PIDFILE": pid_file,
            "PERSISTENT_CHANGES": True,
            "LOG_LEVEL": log_level,
            "LOG_DBG_MODULES": ["*"],
            "YANG_LIB_DIR": yang_mod_dir_env,
            "DATA_JSON_FILE": data_file,
            "VALIDATE_TRANSACTIONS": True,
        }

        http_def = {
            "DOC_ROOT": "doc-root",
            "DOC_DEFAULT_NAME": "index.html",
            "API_ROOT": "/restconf",
            "API_ROOT_RUNNING": "/restconf_running",
            "SERVER_NAME": "jetconf-h2",
            "UPLOAD_SIZE_LIMIT": 1,
            "LISTEN_LOCALHOST_ONLY": listen_on_localhost_only,
            "PORT": port,
            "SERVER_SSL_CERT": ssl_crt,
            "SERVER_SSL_PRIVKEY": ssl_key,
            "DISABLE_SSL": disable_ssl,
            "CA_CERT": ca_crt,
            "DBG_DISABLE_CERTS": False,
        }

        nacm_def = {"ENABLED": True, "ALLOWED_USERS": []}

        root_def = {"GLOBAL": glob_def, "HTTP_SERVER": http_def, "NACM": nacm_def}

        self.glob = glob_def
        self.http = http_def
        self.nacm = nacm_def
        self.root = root_def

        # Shortcuts
        self.api_root_data = None
        self.api_root_running_data = None
        self.api_root_ops = None
        self.api_root_ylv = None

        self._gen_shortcuts()


class Rosettaconf(jetconf.Jetconf):
    def init(self, datamodel: DataModel) -> None:
        usr_conf_data_handlers = ntc_rosetta_conf.usr_conf_data_handlers
        usr_state_data_handlers = ntc_rosetta_conf.usr_state_data_handlers
        usr_op_handlers = ntc_rosetta_conf.usr_op_handlers
        #  usr_action_handlers = None
        usr_datastore = ntc_rosetta_conf.usr_datastore

        self.usr_init = None

        # Datastore init
        datastore = usr_datastore.UserDatastore(
            datamodel, self.config.glob["DATA_JSON_FILE"], with_nacm=False
        )
        self.datastore = datastore
        try:
            datastore.load()
        except (FileNotFoundError, YangsonException) as e:
            raise JetconfInitError(
                'Cannot load JSON data file "{}", reason: {}'.format(
                    self.config.glob["DATA_JSON_FILE"], ErrorHelpers.epretty(e)
                )
            )

        # Validate datastore on startup
        try:
            datastore.get_data_root().validate(ValidationScope.all, ContentType.config)
        except (SchemaError, SemanticError) as e:
            raise JetconfInitError(
                "Initial validation of datastore failed, reason: {}".format(
                    ErrorHelpers.epretty(e)
                )
            )

        usr_conf_data_handlers.register_conf_handlers(datastore)
        usr_state_data_handlers.register_state_handlers(datastore)

        op_internal.register_op_handlers(datastore)
        usr_op_handlers.register_op_handlers(datastore)

        #  usr_action_handlers.register_action_handlers(datastore)

        # Init backend package
        if self.usr_init is not None:
            try:
                self.usr_init.jc_startup()
                self.backend_initiated = True
            except Exception as e:
                raise JetconfInitError(
                    "Backend initialization failed, reason: {}".format(
                        ErrorHelpers.epretty(e)
                    )
                )

        # Create HTTP server
        self.rest_srv = RestServer()
        self.rest_srv.register_api_handlers(datastore)


def start(cfg: RosettaconfConfig, datamodel_name: str) -> None:
    config.CFG = cfg

    try:
        cfg.validate()
    except ValueError as e:
        print("Error: " + str(e))
        sys.exit(1)

    # Set logging level
    log_level = {
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.INFO,
    }.get(cast(str, cfg.glob["LOG_LEVEL"]), logging.INFO)
    logging.root.handlers.clear()

    log_formatter = colorlog.ColoredFormatter(
        "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        },
        secondary_log_colors={},
        style="%",
    )

    log_handler = colorlog.StreamHandler()
    log_handler.setFormatter(log_formatter)
    log_handler.stream = sys.stdout

    logger = colorlog.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(log_level)

    # Print version
    info("NTC Rosetta Conf version {}".format("TBD"))

    # Print configuration
    cfg.print()

    # Instantiate Jetconf main class
    jc = Rosettaconf(cfg)
    jetconf.JC = jc

    try:
        jc.init(get_data_model(datamodel_name))
    except JetconfInitError as e:
        error(str(e))
        jc.cleanup()

        # Exit
        info("Exiting (error)")
        sys.exit(1)

    # Run Jetconf (this will block until shutdown)
    jc.run()

    jc.cleanup()

    # Exit
    info("Exiting")
    sys.exit(0)
