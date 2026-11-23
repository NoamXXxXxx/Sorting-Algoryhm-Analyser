def sort(arr):
    if not arr:
        return
    biggest = max(arr)
    exp = 1
    while biggest // exp > 0:                # one pass per digit
        buckets = [[] for _ in range(10)]
        for i in range(len(arr)):
            buckets[(arr[i] // exp) % 10].append(arr[i])
            yield (i,)
        k = 0
        for bucket in buckets:
            for value in bucket:
                arr[k] = value
                yield (k,)
                k += 1
        exp *= 10
