import argparse
import logging
import docker
import json
import urllib3

from . import config
from .deep_filter import deep_filter

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
        live_attrs = deep_filter(live_container.attrs, config.blacklist)
        staged_attrs = deep_filter(staged_container.attrs, config.blacklist)
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
            # lines1 = json.dumps(live_attrs, indent=4).split("\n")
            # lines2 = json.dumps(staged_attrs, indent=4).split("\n")
            # for l1, l2 in zip(lines1, lines2):
            #     prefix = "\x1b[1m" if (l1 != l2) else ""
            #     suffix = "\x1b[0m" if (l1 != l2) else ""
            #     if l1 != l2:
            #         print("%s%-80s%-80s%s" % (prefix, l1, l2, suffix))
            logger.info("%s: stopping", live_container.name)
            live_container.stop()
            logger.info("%s: removing", live_container.name)
            live_container.remove()
            logger.info("%s: renaming to %s", staged_container.name, args.live)
            staged_container.rename(args.live)
            logger.info("%s: starting", args.live)
            staged_container.start()
