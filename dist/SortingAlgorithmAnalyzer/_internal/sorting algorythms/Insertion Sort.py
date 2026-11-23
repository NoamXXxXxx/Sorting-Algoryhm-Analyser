def sort(arr):
    for i in range(1, len(arr)):
        j = i
        while j > 0:
            yield (j - 1, j)
            if arr[j - 1] > arr[j]:
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
                j -= 1
            else:
                break
