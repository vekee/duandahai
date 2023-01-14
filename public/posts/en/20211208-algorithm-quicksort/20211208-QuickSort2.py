# change the position on each number
def swapEachOther(arr, leftIndex, rightIndex):
    tmp = arr[leftIndex]
    arr[leftIndex] = arr[rightIndex]
    arr[rightIndex] = tmp
    print(arr)

# quck sort method : 
def sort(arr, startIndex, endIndex):
    if startIndex >= endIndex:
        return

    # set the last number as the pivot number
    pivotIndex = endIndex

    # set the partitionIndex before the startIndex
    partitionIndex = startIndex -1

    # change the positon when it smaller than pivot number from left
    for i in  range(startIndex, endIndex):
        if arr[i] <= arr[pivotIndex]:
            # move the smaller number to the left of bigger number than pivot
            partitionIndex = partitionIndex + 1
            swapEachOther(arr, partitionIndex, i)
    
    # get the partitionIndex that will be cut the array in half
    partitionIndex = partitionIndex + 1

    # move the pivot to the middle posotion
    swapEachOther(arr, partitionIndex, pivotIndex)
    
    # use the sort method on left half array
    sort(arr, startIndex, partitionIndex - 1)
    # use the sort method on right half array
    sort(arr, partitionIndex + 1, endIndex)

arr = [3, 1, 2, 9, 4, 10, 5, 8, 6, 7]
print(arr)
sort(arr, 0, len(arr) -1)
