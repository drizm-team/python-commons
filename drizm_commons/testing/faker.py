import io
import random
import string
from typing import Optional, Sequence

from PIL import Image


def random_flat_colored_image(size_x: int,
                              size_y: int,
                              ext: Optional[str] = "jpeg",
                              ) -> io.BytesIO:
    file = io.BytesIO()
    image = Image.new(
        "RGB",
        size=(size_x, size_y),
        color=random_rgb_color()
    )
    image.save(file, ext)

    return file


def random_hex_color() -> str:
    return "#%06x" % random.randint(0, 0xFFFFFF)


def random_rgb_color() -> tuple:
    return tuple(  # generate a random RGB color
        random.randint(0, 255) for _ in range(3)
    )


def random_email_address(top_level_domain: Optional[str] = "com",
                         choice_sequence: Optional[Sequence] = string.ascii_letters
                         ) -> str:
    prefix = ''.join(random.choices(choice_sequence, k=12))
    domain = ''.join(random.choices(choice_sequence, k=8))
    return f"{prefix}@{domain}.{top_level_domain}"


__all__ = [
    "random_flat_colored_image",
    "random_hex_color", "random_rgb_color",
    "random_email_address"
]
