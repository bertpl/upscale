"""
Ugly hack to make sure transformers tqdm progress bar is never shown.  Otherwise, at every call to a pipeline or
when loading a pipline, we get a separate progress bar, which will unnecessarily clutter the console.

Import this module to make sure it is applied globally.
"""

import tqdm
from tqdm import auto

_orig_tqdm = tqdm.tqdm


def my_tqdm(iterable, *args, **kwargs):
    # Override tqdm to do nothing in certain cases
    if ("Loading pipeline components" in kwargs.get("desc", "")) or (kwargs.get("desc", "") == ""):
        return iterable  # no tqdm, just return the iterable as is
    else:
        # For all other cases, return a regular tqdm instance
        return _orig_tqdm(iterable, *args, **kwargs)


tqdm.tqdm = my_tqdm
auto.tqdm = my_tqdm
