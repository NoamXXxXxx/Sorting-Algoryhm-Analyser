def sort(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        swapped = False
        for i in range(lo, hi):              # left -> right
            yield (i, i + 1)
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        hi -= 1
        swapped = False
        for i in range(hi, lo, -1):          # right -> left
            yield (i - 1, i)
            if arr[i - 1] > arr[i]:
                arr[i - 1], arr[i] = arr[i], arr[i - 1]
                swapped = True
        if not swapped:
            break
        lo += 1
