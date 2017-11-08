import pytest

import rivalcfg.helpers


class TestIntToLittleEndianBytearray(object):

    def test_small_number_16bit(self):
        assert rivalcfg.helpers.uint_to_little_endian_bytearray(0x0001, 2) == [0x01, 0x00]  # noqa

    def test_bigger_number_16bit(self):
        assert rivalcfg.helpers.uint_to_little_endian_bytearray(0x0a01, 2) == [0x01, 0x0a]  # noqa

    def test_overflow_number_16bit(self):
        assert rivalcfg.helpers.uint_to_little_endian_bytearray(0xFFFF, 2) == [0xFF, 0xFF]  # noqa
        with pytest.raises(ValueError):
            rivalcfg.helpers.uint_to_little_endian_bytearray(0xABCDEF, 2)
