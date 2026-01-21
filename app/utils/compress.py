# for now passthrough. later we'll implement Pillow-based compression loop.
def compress_file(data: bytes, filename: str):
    # return original bytes, same filename
    return data, filename
