import math


def chuncked_lenght(list_that_will_be_chuncked: list, size_of_chunk: int) -> int:
    length_of_list = len(list_that_will_be_chuncked)
    length_of_chunk = math.floor(length_of_list / size_of_chunk)
    if (length_of_list % size_of_chunk) != 0:
        length_of_chunk += 1
    return length_of_chunk
