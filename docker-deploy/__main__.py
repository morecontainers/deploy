import argparse
import logging
import docker
import json
import urllib3

from . import config
from . import dict_filter

urllib3.disable_warnings()

parser = argparse.ArgumentParser(
    prog="docker-redeploy", description="redeploy Docker containers"
)
parser.add_argument("live", help="live production container")
parser.add_argument("staged", help="staged container")
args = parser.parse_args()
client = docker.from_env()
logger = logging.getLogger("docker-redeploy")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
# Get containers
try:
    live_container = client.containers.get(args.live)
except docker.errors.NotFound:
    logger.error("%s container not found", arg.live)
else:
    try:
        staged_container = client.containers.get(args.staged)
    except docker.errors.NotFound:
        logger.error("%s container not found", args.staged)
    else:
        # Get container attributes
        live_attrs = dict_filter(live_container.attrs, config.blacklist)
        staged_attrs = dict_filter(staged_container.attrs, config.blacklist)
        # Attributes are equal: no redeploy; but remove staging container
        if live_attrs == staged_attrs:
            logger.info("%s: redeployment not needed", args.live)
            logger.info("%s: removing", args.staged)
            try:
                staged_container.remove()
                logger.info("%s: removed", args.staged)
            except:
                logger.exception()
        else:
            logging.info("redeploy %s from %s", args.live, args.staged)
            logger.info("%s: stopping", live_container.name)
            live_container.stop()
            logger.info("%s: removing", live_container.name)
            live_container.remove()
            logger.info("%s: renaming to %s", staged_container.name, args.live)
            staged_container.rename(args.live)
            logger.info("%s: starting", args.live)
            staged_container.start()
