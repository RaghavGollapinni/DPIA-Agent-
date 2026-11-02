import re
import zlib

import numpy as np
import pytest

STOP = {"the", "a", "an", "of", "to", "and", "or", "is", "are", "be", "in", "for", "on", "with", "that",
        "this", "it", "as", "by", "at", "from", "must", "can", "may", "any", "their", "they", "you"}


def fake_embedder(texts):
    """Hashed bag-of-words. A stand-in for MiniLM so tests run offline and fast."""
    out = np.zeros((len(texts), 1024), dtype="float32")
    for row, text in enumerate(texts):
        for word in re.findall(r"[a-z']+", text.lower()):
            if word not in STOP:
                out[row, zlib.crc32(word.encode()) % 1024] += 1.0
    return out


@pytest.fixture
def embedder():
    return fake_embedder
