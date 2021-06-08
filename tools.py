def partition(l, low, high):
    i = low - 1
    pivot = l[high]["free"]

    for j in range(low, high):
        if l[j]["free"] > pivot:
            i += 1
            l[i], l[j] = l[j], l[i]
    i += 1
    l[i], l[high] = l[high], l[i]
    return i


def sort_balances(l):
    quicksort(l, 0, len(l) - 1)


def quicksort(l, low, high):
    if len(l) == 1:
        return l
    if low < high:
        p = partition(l, low, high)
        quicksort(l, low, p - 1)
        quicksort(l, p + 1, high)
