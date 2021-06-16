import os
import random
import struct
import sys
import binascii

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from crccheck.crc import Crc32

from utils.logger import logger
from utils.file_utils import force_make


if sys.version_info < (3,):

    def get_bytes(x):
        return x


else:

    def get_bytes(x):
        if type(x) is str:
            return bytes(x, "utf-8")
        else:
            return bytes(x)


BLOCK_SIZE = 16  # Bytes


def pad(s):
    return get_bytes(s) + get_bytes(
        chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
        * (BLOCK_SIZE - len(s) % BLOCK_SIZE)
    )


class FirmwareInfo:
    def __init__(self, checksum, size, type, version):
        self.checksum = checksum
        self.size = size
        self.type = type
        self.version = version

    def __str__(self):
        return "Size: {0}, checksum {1}, type: {2}, version: {3}".format(
            hex(self.size),
            hex(self.checksum),
            hex(self.type),
            hex(self.version),
        )

    def serialize(self):
        serialized_fw_info = bytearray(16)
        struct.pack_into(
            "<IIII",
            serialized_fw_info,
            0,
            self.checksum,
            self.size,
            self.type,
            self.version,
        )
        return serialized_fw_info


def calculate_fw_info(input_file, fw_type, fw_version):
    with open(input_file, "rb") as f:
        # Slurp the whole file and efficiently convert it to hex all at once
        hexdata = f.read()
        fw_size = len(hexdata)

    crc_calculator = Crc32()
    
    crc_calculator.process(
        bytearray(
            struct.pack("<I", fw_size)
            + struct.pack("<I", fw_type)
            + struct.pack("<I", fw_version)
            + hexdata
        )
    )
    fw_checksum = crc_calculator.final()
    
    
    # fw_info = bytearray(16)
    # struct.pack_into('<IIII', fw_info, 0, fw_checksum,
    #                  fw_size, fw_type, fw_version)
    fw_info = FirmwareInfo(fw_checksum, fw_size, fw_type, fw_version)
    return fw_info


def write_fw_info(fw_info, offset, input_file, output_file):
    serialized_fw_info = fw_info.serialize()
    force_make(os.path.dirname(output_file))
    with open(output_file, "wb") as f:
        f.write(serialized_fw_info)
        remain_byte = offset - len(serialized_fw_info)
        # logging.debug('Remain byte to write: {}'.format(remain_byte))
        if remain_byte > 0:
            f.write(b"\xff" * remain_byte)
        with open(input_file, "rb") as f2:
            f.write(bytearray(f2.read()))

def write_mbr_info(fw_info, mbr_file):
    serialized_fw_info = fw_info.serialize()
    force_make(os.path.dirname(mbr_file))
    with open(mbr_file, "wb") as f:
        f.write(serialized_fw_info)


def encrypt_byte(input_data, key, iv):
    backend = default_backend()
    cipher = Cipher(
        algorithms.AES(get_bytes(key)),
        modes.CBC(get_bytes(iv)),
        backend=backend,
    )
    encryptor = cipher.encryptor()

    # convert input to bytes
    input_bytes = get_bytes(input_data)
    # add padding
    input_bytes = pad(input_bytes)
    output = encryptor.update(input_bytes) + encryptor.finalize()
    return output


def encrypt_file(in_filename, key, iv, out_filename=None, chunksize=64 * 1024):
    if not out_filename:
        out_filename = in_filename + ".enc"
    force_make(os.path.dirname(out_filename))
    backend = default_backend()
    cipher = Cipher(
        algorithms.AES(get_bytes(key)),
        modes.CBC(get_bytes(iv)),
        backend=backend,
    )
    encryptor = cipher.encryptor()

    totalSize = os.path.getsize(in_filename)
    with open(in_filename, "rb") as infile:
        with open(out_filename, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                chunk_length = len(chunk)
                logger.debug("Read {} byte from input".format(chunk_length))
                totalSize -= chunk_length
                if chunk_length == 0:
                    break
                elif totalSize == 0:
                    logger.info("Last buffer, add padding byte")
                    logger.debug("Current chunk size: {}".format(chunk_length))
                    chunk = pad(chunk)
                    logger.debug(
                        "Chunk size after add padding: {}".format(len(chunk))
                    )

                outfile.write(encryptor.update(chunk))
