import os

def split_file(data: bytes, fragment_size=1024*1024):
    fragments = []
    for i in range(0, len(data), fragment_size):
        fragments.append(data[i:i+fragment_size])
    return fragments

def merge_fragments(fragments: list) -> bytes:
    return b"".join(fragments)
