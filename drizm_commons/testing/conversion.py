import base64
import io


def image_file_b64(image_file: io.BytesIO) -> bytes:
    return base64.b64encode(image_file.getvalue())


__all__ = ["image_file_b64"]
