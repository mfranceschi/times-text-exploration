from utilities import create_empty_file_with_size

import mmap

name = "temporary.txt"
size = 10 * 1024 * 1024

create_empty_file_with_size(file=name, size=size)

with open(name, mode="wb+", buffering=0) as file:

    with mmap.mmap(file.fileno(), length=size, access=mmap.ACCESS_DEFAULT, offset=0) as a:
        a[:4] = b"abcd"
        print(a[:4])
        pass
