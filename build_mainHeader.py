import argparse
import sys
import os
import binascii
import json

from utils.logger import logger
from helpers.helpers import (
    encrypt_file,
    calculate_fw_info,
    write_fw_info,
    write_mbr_info,
    encrypt_byte,
    pad,
)


def main(args_):
    parser = argparse.ArgumentParser(
        description="This script generate application master boot record"
    )
    parser.add_argument(
        "--cfg",
        dest="config_file",
        default="./config/config.json",
        help="configuration file",
    )
    args = parser.parse_args(args_)
    with open(args.config_file) as json_file:
        config = json.load(json_file)

    # convert input config to variable
    input_binary = config["input_binary"]
    output_mainHeader_file = config["output_mainHeader_file"]
    fw_type = int(config["fw_type"], 16)
    fw_version = int(config["fw_version"], 16)

    logger.debug("input_binary: {0}".format(input_binary))
    logger.debug("output_mainHeader_file: {0}".format(output_mainHeader_file))
    logger.debug("fw_type: {0}".format(fw_type))
    logger.debug("fw_version: {0}".format(fw_version))

    logger.info("-" * 80)
    logger.info("Start calculate firmware info...")
    fw_info = calculate_fw_info(input_binary, fw_type, fw_version)
    logger.info("Finish calculate firmware info")
    logger.debug("Firmware info:")
    logger.debug(fw_info)

    logger.info("-" * 80)
    logger.info("Start write final mbr file...")
    # TODO
    write_mbr_info(fw_info, output_mainHeader_file)
    logger.info("Finish write final mbr file")


if __name__ == "__main__":
    current_dir = os.getcwd()
    relative_path = os.path.dirname(__file__)
    if relative_path != '':
        os.chdir(relative_path)
    main(sys.argv[1:])
    os.chdir(current_dir)
