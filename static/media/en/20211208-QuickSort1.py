# change the position on each number
def swapEachOther(arr, leftIndex, rightIndex):
    tmp = arr[leftIndex]
    arr[leftIndex] = arr[rightIndex]
    arr[rightIndex] = tmp
    print(arr)

# quck sort method : start from first number by pivot
def sort(arr, startIndex, endIndex):
    if startIndex >= endIndex:
        return

    leftIndex = startIndex
    rightIndex = endIndex

    # set the first pivot by first number
    compareValue = arr[startIndex]

    while leftIndex < rightIndex:
        # find the next pivot that was smaller than compareValue from right
        while leftIndex < rightIndex and arr[rightIndex] > compareValue:
            rightIndex = rightIndex - 1
        
        # find the next pivot that was bigger than compareValue from left
        while leftIndex < rightIndex and arr[leftIndex] <= compareValue:
            leftIndex = leftIndex + 1

        # while finding the next pivot, move smaller number to left and move bigger number to right
        if leftIndex < rightIndex:
            swapEachOther(arr, leftIndex, rightIndex)

    # move the pivot to the middle posotion
    swapEachOther(arr, startIndex, rightIndex)
    # use the sort method on left half array
    sort(arr, startIndex, rightIndex - 1)
    # use the sort method on right half array
    sort(arr, rightIndex + 1, endIndex)


arr = [3, 1, 2, 9, 4, 10, 5, 8, 6, 7]
print(arr)
sort(arr, 0, len(arr) -1)
