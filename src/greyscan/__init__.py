"""Gray Bar Scanner package."""

__version__ = "0.0.1"

__all__ = [
    "batch_scan_images",
    "scan_image_for_gray_bands",
    "is_gray_band",
]

def __getattr__(name):
    if name in __all__:
        from . import scanner
        return getattr(scanner, name)
    raise AttributeError(name)
