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
    encrypt_byte,
    pad,
)


def main(args_):
    parser = argparse.ArgumentParser(
        description="This script encrypt firmware with aes algorithm."
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
    output_file = config["output_file"]
    fw_type = int(config["fw_type_dfu"], 16)
    fw_version = int(config["fw_version"], 16)
    aes_key = bytes(bytearray.fromhex(config["aes-key"]))
    aes_iv = bytes(bytearray.fromhex(config["aes-iv"]))

    logger.debug("input_binary: {0}".format(input_binary))
    logger.debug("output_file: {0}".format(output_file))
    logger.debug("fw_type: {0}".format(fw_type))
    logger.debug("fw_version: {0}".format(fw_version))

    logger.info("-" * 80)
    logger.info("Start encrypt firmware...")
    encrypted_file = "main_app_enc.bin"
    encrypt_file(input_binary, aes_key, aes_iv, encrypted_file)
    logger.info("Finish encrypt firmware...")

    logger.info("-" * 80)
    logger.info("Start calculate encrypted firmware info...")
    encrypted_fw_info = calculate_fw_info(encrypted_file, fw_type, fw_version)
    logger.info("Finish calculate firmware version")
    logger.debug("Firmware info:")
    logger.debug(encrypted_fw_info)

    logger.info("-" * 80)
    logger.info("Start write final encrypted file...")
    # TODO
    write_fw_info(encrypted_fw_info, 16, encrypted_file, output_file)
    logger.info("Finish write final encrypted file")
    
    # remove file encrypt temp
    os.remove(encrypted_file)


if __name__ == "__main__":
    current_dir = os.getcwd()
    relative_path = os.path.dirname(__file__)
    if relative_path != '':
        os.chdir(relative_path)
    main(sys.argv[1:])
    os.chdir(current_dir)
