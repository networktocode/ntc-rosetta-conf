import click

from ntc_rosetta_conf import server


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option(
    "--datamodel",
    type=click.Choice(["openconfig", "ntc"]),
    default="openconfig",
    help="Datamodel to use",
)
@click.option("--pid-file", default="/tmp/ntc-rosetta-conf.pid", help="PID file")
@click.option(
    "--log-level",
    type=click.Choice(["debug", "info", "warning", "error"]),
    default="info",
    help="Logging level",
)
@click.option(
    "--data-file",
    default="data.json",
    help="Path to json file to load data from and save on commit",
)
@click.option(
    "--listen-on-localhost-only",
    is_flag=True,
    default=False,
    help="Listen on localhost only",
)
@click.option("--disable-ssl", is_flag=True, default=False, help="Disable SSL")
@click.option("--port", default=8443, help="Port to listen to")
@click.option("--ssl-crt", default="ssl.crt", help="SSL Certificate for the webserver")
@click.option("--ssl-key", default="ssl.key", help="Private key for the webserver")
@click.option(
    "--ca-crt", default="ca.pem", help="CA certificate used to sign client certificates"
)
def serve(
    datamodel: str,
    pid_file: str,
    log_level: str,
    data_file: str,
    listen_on_localhost_only: bool,
    port: int,
    ssl_crt: str,
    ssl_key: str,
    ca_crt: str,
    disable_ssl: bool,
) -> None:
    cfg = server.RosettaconfConfig(
        log_level=log_level,
        pid_file=pid_file,
        data_file=data_file,
        listen_on_localhost_only=listen_on_localhost_only,
        port=port,
        ssl_crt=ssl_crt,
        ssl_key=ssl_key,
        ca_crt=ca_crt,
        disable_ssl=disable_ssl,
    )
    server.start(cfg, datamodel)


if __name__ == "__main__":
    cli()
