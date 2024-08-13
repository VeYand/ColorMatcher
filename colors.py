def rgb_to_lab(rgb_color: (int, int, int)) -> (float, float, float):
    r, g, b = rgb_color
    r /= 255.0
    g /= 255.0
    b /= 255.0

    r, g, b = (c ** 2.2 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b))

    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    x = x / 0.95047
    z = z / 1.08883

    x = x ** (1 / 3) if x > 0.008856 else (903.3 * x + 16) / 116
    y = y ** (1 / 3) if y > 0.008856 else (903.3 * y + 16) / 116
    z = z ** (1 / 3) if z > 0.008856 else (903.3 * z + 16) / 116

    l = max(0, 116 * y - 16)
    a = max(-128, min(127, 500 * (x - y)))
    b = max(-128, min(127, 200 * (y - z)))

    return l, a, b


def compare_colors(color1: (int, int, int), color2: (int, int, int)) -> float:
    lab_color1 = rgb_to_lab(color1)
    lab_color2 = rgb_to_lab(color2)

    delta_l = lab_color1[0] - lab_color2[0]
    delta_a = lab_color1[1] - lab_color2[1]
    delta_b = lab_color1[2] - lab_color2[2]

    delta_e = (delta_l ** 2 + delta_a ** 2 + delta_b ** 2) ** 0.5

    return delta_e
