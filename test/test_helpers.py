import pytest

import rivalcfg.helpers


class TestIntToLittleEndianBytearray(object):

    def test_small_number_16bit(self):
        assert rivalcfg.helpers.uint_to_little_endian_bytearray(0x0001, 2) == bytearray([0x01, 0x00])

    def test_bigger_number_16bit(self):
        assert rivalcfg.helpers.uint_to_little_endian_bytearray(0x0a01, 2) == bytearray([0x01, 0x0a])

    def test_ouverflow_number_16bit(self):
        assert rivalcfg.helpers.uint_to_little_endian_bytearray(0xFFFF, 2) == bytearray([0xFF, 0xFF])
        with pytest.raises(ValueError):
            rivalcfg.helpers.uint_to_little_endian_bytearray(0xABCDEF, 2)
