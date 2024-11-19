def float_to_fixed_bytes(value, min_value, max_value, length=4):
    if not (min_value <= value <= max_value):
        return b"\xFF" * length

    normalized_value = (value - min_value) / (max_value - min_value)
    max_int_value = (1 << (length * 8)) - 1
    scaled_value = int(normalized_value * max_int_value)

    return scaled_value.to_bytes(length, byteorder="big")


def fixed_bytes_to_float(byte_representation, min_value, max_value):
    scaled_value = int.from_bytes(byte_representation, byteorder="big")
    max_int_value = (1 << (len(byte_representation) * 8)) - 1
    normalized_value = scaled_value / max_int_value

    return normalized_value * (max_value - min_value) + min_value
