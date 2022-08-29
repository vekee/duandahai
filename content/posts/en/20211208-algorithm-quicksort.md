+++
author = "DUAN DAHAI"
title = "Two ways of create a quicksort algorithm by Python"
date = "2021-12-08"
description = "Two ways of create a quicksort algorithm by Python"
tags = [
    "algorithm",
    "quicksort",
    "Python"
]
categories = [
    "Python",
    "algorithm"
]
+++

In a quick sort algorithm, 
It picks an element as a pivot and partitions the given array around the picked pivot. (For sort by ascending, it moves smaller number to the pivot's left, and it moves bigger number to the pivot's right)

I wrote two classic samples by use python.
- Always pick the first element as a pivot.
- Always pick the last element as a pivot.


#### This is a sample for quick sort that start from left value as pivot
```PYTHON
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
```

#### This is a sample for quick sort that start from right number as pivot

```PYTHON
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
```

You can click 
<a href="/media/en/20211208-QuickSort1.py" >here(QuickSort1)</a>
, 
<a href="/media/en/20211208-QuickSort2.py" >here(QuickSort2)</a>
to download the SBL Excle.
