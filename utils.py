from math import ceil


def slice_by_size(content_length, chunk_size):
    start = 0
    while start < content_length:
        end = min(start + chunk_size, content_length)
        yield start // chunk_size, start, end - 1
        start = end


def slice_by_count(content_length, chunk_count):
    start = 0
    chunk_size = ceil(content_length / chunk_count)
    while start < content_length:
        end = min(start + chunk_size, content_length)
        yield start // chunk_size, start, end - 1
        start = end


if __name__ == '__main__':
    content_length = 1654545132
    chunk_size = 1024 * 1024 * 100
    chunk_count = 16
    print(*slice_by_size(content_length, chunk_size))
    print(*slice_by_count(content_length, chunk_count))
