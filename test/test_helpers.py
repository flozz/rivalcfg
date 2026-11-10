import pytest

from rivalcfg import helpers


class TestUintToLittleEndianBytearray(object):
    def test_negative_number_raises(self):
        with pytest.raises(ValueError, match="integer overflow"):
            helpers.uint_to_little_endian_bytearray(-1, 1)

    def test_large_negative_number_raises(self):
        with pytest.raises(ValueError, match="integer overflow"):
            helpers.uint_to_little_endian_bytearray(-256, 2)

    def test_zero_still_works(self):
        assert helpers.uint_to_little_endian_bytearray(0, 1) == [0]

    def test_positive_values_unchanged(self):
        assert helpers.uint_to_little_endian_bytearray(0x42, 1) == [66]
        assert helpers.uint_to_little_endian_bytearray(0xFF42, 2) == [66, 255]
