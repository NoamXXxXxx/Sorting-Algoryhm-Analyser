def sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):      # build max-heap
        yield from sift_down(arr, i, n)
    for end in range(n - 1, 0, -1):          # move max to the end
        arr[0], arr[end] = arr[end], arr[0]
        yield (0, end)
        yield from sift_down(arr, 0, end)


def sift_down(arr, root, size):
    while True:
        child = 2 * root + 1
        if child >= size:
            return
        if child + 1 < size:
            yield (child, child + 1)
            if arr[child + 1] > arr[child]:
                child += 1
        yield (root, child)
        if arr[root] >= arr[child]:
            return
        arr[root], arr[child] = arr[child], arr[root]
        root = child
