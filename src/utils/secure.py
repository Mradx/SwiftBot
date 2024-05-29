import os
import re


def secure_filename(filename: str) -> str:
    _filename_strip_re = re.compile(r"[^\w\s.-]", re.U)
    _windows_device_files = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(10)),
        *(f"LPT{i}" for i in range(10)),
    }

    filename = _filename_strip_re.sub("", filename).strip()

    for sep in os.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")

    if os.name == "nt" and filename and filename.split(".")[0].upper() in _windows_device_files:
        filename = f"_{filename}"

    filename = " ".join(filename.split())

    return filename
