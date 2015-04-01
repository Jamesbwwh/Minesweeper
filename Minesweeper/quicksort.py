#String = list("EASYQUESTION")

def Partition(a):
    pivot = a[0]
    pivotIndex = 0
    N = len(a)
    for i in range(1,N):
        if a[i] < pivot:
            pivotIndex += 1
            a[i], a[pivotIndex] = a[pivotIndex], a[i]
    a[0], a[pivotIndex] = a[pivotIndex], a[0]
    return pivotIndex

def QuickSort(a):
    N = len(a)
    if N > 1:
        pivotIndex = Partition(a)
        a[:pivotIndex] = QuickSort(a[:pivotIndex])
        a[pivotIndex + 1:] = QuickSort(a[pivotIndex + 1:])
    return a

#print String, "\n"
#print QuickSort(String)