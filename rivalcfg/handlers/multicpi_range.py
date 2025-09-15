"""
The 'multicpi_range' type configures multiple CPI presets for devices like the Rival 3 Gen 2, supporting:
- Single CPI values (X=Y) via -s/--sensitivity (up to 5 presets, max_preset_count=5).
- Independent X,Y CPI pairs via -sxy/--sensitivity-xy (up to 4 pairs, max_preset_count=4).

Packet structure:
- max_preset_count=5: `[CPI_count [1-5], CPI_selected [0-4], CPI_1, ..., CPI_N]` (2+N bytes, no padding)
- sensitivity_mode=xy, single pair: `[0x34, CPI_count=1, CPI_selected=0, CPI_X, CPI_Y]` (5 bytes, no padding)
- sensitivity_mode=xy, multi-pair (2 presets): `[0x34, CPI_count=2, CPI_selected [0-1], CPI_1_X, CPI_1_Y, CPI_2_X, CPI_2_Y]` (7 bytes, no padding)
- sensitivity_mode=xy, multi-pair (4 presets): `[0x34, CPI_count=4, CPI_selected [0-3], CPI_1_X, CPI_1_Y, ..., CPI_4_X, CPI_4_Y]` (11 bytes, no padding)

"""

import re
import argparse
import math

from ..helpers import merge_bytes, uint_to_little_endian_bytearray

def process_value(setting_info, value, selected_preset=None):
    """Process a multicpi_range setting."""
    mappings = {
        100: 0x03,
        200: 0x04,
        400: 0x08,
        800: 0x14,
        1200: 0x1b,
        1600: 0x24,
        2400: 0x37,
        3200: 0x4C
    }
    cpi_pairs = []

    # Parse input value
    if isinstance(value, (int, float)):
        cpi_pairs = [[int(value), int(value)]]
    elif isinstance(value, (list, tuple)):
        cpi_pairs = [[int(x), int(y)] for x, y in value]
    else:
        sensitivity_mode = setting_info.get("sensitivity_mode", "single")
        if sensitivity_mode == "single":
            value = value.replace(" ", "")
            presets = value.split(",")
            cpi_pairs = []
            for preset in presets:
                if preset:
                    cpi_val = int(preset)
                    cpi_pairs.append([cpi_val, cpi_val])
        else:
            value = value.replace(" ", "")
            presets = value.split(",")
            cpi_pairs = []
            for preset in presets:
                if preset:
                    match = re.match(r"^(\d+)x(\d+)$", preset)
                    if not match:
                        raise ValueError(f"Invalid CPI pair format '{preset}', expected 'CPI_XxCPI_Y'")
                    cpi_x, cpi_y = map(int, match.groups())
                    cpi_pairs.append([cpi_x, cpi_y])

    # Preserve duplicates for single CPI mode, deduplicate for xy mode
    sensitivity_mode = setting_info.get("sensitivity_mode", "single")
    if sensitivity_mode == "single":
        final_pairs = cpi_pairs
        for cpi_x, cpi_y in final_pairs:
            if cpi_x != cpi_y:
                raise ValueError(f"Single CPI mode (-s) requires X=Y, got {cpi_x}x{cpi_y}")
    else:
        unique_pairs = []
        seen = set()
        for pair in cpi_pairs:
            pair_tuple = tuple(pair)
            if pair_tuple not in seen:
                unique_pairs.append(pair)
                seen.add(pair_tuple)
        final_pairs = unique_pairs
        #if len(final_pairs) == 1:
            #print("Single pair detected, keeping CPI_count=1")

    # Define max_presets early
    max_presets = 4 if sensitivity_mode == "xy" else setting_info["max_preset_count"]

    cpi_count = len(final_pairs)
    if len(final_pairs) > max_presets:
        final_pairs = final_pairs[:max_presets]
        print(f"Warning: Truncated to {max_presets} presets: {final_pairs}")
    elif len(final_pairs) < max_presets:
        print(f"Warning: Using {len(final_pairs)} presets, expected up to {max_presets}: {final_pairs}")

    # Debug: Print parsed presets
    #print(f"Parsed CPI presets: {final_pairs}")

    # Selected preset
    if selected_preset is None:
        selected_preset = 0 if len(final_pairs) == 1 else 0
    else:
        selected_preset += setting_info["first_preset"] - 1

    # Checks
    if len(final_pairs) == 0:
        raise ValueError("You must provide at least one CPI preset")

    if not 0 <= selected_preset < len(final_pairs):
        raise ValueError(f"The selected preset {selected_preset} is out of range for {len(final_pairs)} presets")

    if "first_preset" not in setting_info:
        raise ValueError("Missing 'first_preset' parameter for 'multicpi_range' handler")

    if "cpi_length_byte" not in setting_info:
        raise ValueError("Missing 'cpi_length_byte' parameter for 'multicpi_range' handler")

    if "count_mode" not in setting_info:
        raise ValueError("Missing 'count_mode' parameter for 'multicpi_range' handler")

    if setting_info["count_mode"] not in ("number", "flag"):
        raise ValueError(f"Invalid 'count_mode' parameter '{setting_info['count_mode']}'")

    cpi_length = setting_info["cpi_length_byte"]
    count_mode = setting_info["count_mode"]

    # Calculate CPI count
    if count_mode == "flag":
        cpi_count = 0b11111111 >> (8 - cpi_count)

    # Store cpi_count in setting_info
    setting_info["cpi_count"] = cpi_count

    # Pre-reset for -sxy to clear firmware state
    if sensitivity_mode == "xy":
        reset_packet = [0x34, 0x1, 0x0, 0x8, 0x8]  # Reset to 400x400
        #print(f"Sending pre-reset packet: {list(map(hex, reset_packet))}")
        # Note: This requires mouse.py to send the packet

    # Process CPI values and construct packet
    output_values = []
    if sensitivity_mode == "xy":
        # Single pair: 5-byte packet
        if len(final_pairs) == 1:
            cpi_x, cpi_y = final_pairs[0]
            if cpi_x not in mappings or cpi_y not in mappings:
                raise ValueError(f"Unsupported CPI value: {cpi_x}x{cpi_y}")
            x_value = mappings[cpi_x]
            y_value = mappings[cpi_y]
            x_bytes = uint_to_little_endian_bytearray(x_value, cpi_length)
            y_bytes = uint_to_little_endian_bytearray(y_value, cpi_length)
            output_values = merge_bytes(x_bytes, y_bytes)
            #print(f"Mapped CPI {cpi_x}x{cpi_y} to X={x_value} (0x{x_value:02X}), Y={y_value} (0x{y_value:02X})")
            packet = merge_bytes(0x34, cpi_count, selected_preset, output_values)
        else:
            # Multi-pair: 7-byte packet for 2 presets, 11-byte for 4 presets
            for cpi_x, cpi_y in final_pairs:
                if cpi_x not in mappings or cpi_y not in mappings:
                    raise ValueError(f"Unsupported CPI value: {cpi_x}x{cpi_y}")
                x_value = mappings[cpi_x]
                y_value = mappings[cpi_y]
                x_bytes = uint_to_little_endian_bytearray(x_value, cpi_length)
                y_bytes = uint_to_little_endian_bytearray(y_value, cpi_length)
                output_values = merge_bytes(output_values, x_bytes, y_bytes)
                #print(f"Mapped CPI {cpi_x}x{cpi_y} to X={x_value} (0x{x_value:02X}), Y={y_value} (0x{y_value:02X})")
            packet = merge_bytes(0x34, cpi_count, selected_preset, output_values)
    else:
        for cpi_x, cpi_y in final_pairs:
            if cpi_x not in mappings:
                raise ValueError(f"Unsupported CPI value: {cpi_x}")
            value = mappings[cpi_x]
            value_bytes = uint_to_little_endian_bytearray(value, cpi_length)
            output_values = merge_bytes(output_values, value_bytes)
            #print(f"Mapped CPI {cpi_x}x{cpi_y} to {value} (0x{value:02X})")
        packet = merge_bytes(cpi_count, selected_preset, output_values)

    #print(f"Generated packet: {list(map(hex, packet))}")
    return packet

def cli_multirange_validator(max_preset_count, sensitivity_mode="single"):
    class CheckMultiCpiRange(argparse.Action):
        """Validate value from CLI"""
        def __call__(self, parser, namespace, value, option_string=None):
            max_allowed = 4 if sensitivity_mode == "xy" else max_preset_count
            pattern = (
                r"^ *(?:\d+x\d+)(?: *, *(?:\d+x\d+)){0,%i} *$"
                if sensitivity_mode == "xy" else
                r"^ *\d+(?: *, *\d+){0,%i} *$"
            ) % (max_allowed - 1)
            if not re.match(pattern, value):
                raise argparse.ArgumentError(self, f"Invalid CPI list: '{value}'")
            setattr(namespace, self.dest.upper(), value)
    return CheckMultiCpiRange


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the multicpi_range setting to the CLI parser."""
    max_presets = 4 if setting_info.get("sensitivity_mode", "single") == "xy" else setting_info["max_preset_count"]
    sensitivity_mode = setting_info.get("sensitivity_mode", "single")
    default_value = setting_info.get("default", "None")
    description = "%s (up to %i settings, from %i cpi to %i cpi, default: %s)" % (
        setting_info["description"],
        max_presets,
        setting_info["input_range"][0],
        setting_info["input_range"][1],
        default_value,
    )
    cli_parser.add_argument(
        *setting_info["cli"],
        help=description,
        dest=setting_name.upper(),
        metavar=setting_name.upper(),
        action=cli_multirange_validator(max_preset_count=max_presets, sensitivity_mode=sensitivity_mode),
    )
