# 1.
class Solution(object):
    def findLengthOfLCIS(self, values):
        if not values:
            return 0
        streak = 1
        longest = 1
        for index in range(1, len(values)):
            if values[index] > values[index - 1]:
                streak += 1
            else:
                streak = 1
            longest = max(longest, streak)
        return longest




# This function finds the longest increasing sequence in the arra 
# I keep a streak to count how long the current sequence is
# If the current number is bigger than the previous one, I add 1 to streak
# If it’s not, I reset streak to 1 
# After each step, I compare streak with longest, which tracks the maximum, and update longest if needed. At the end, I return longest


#  2.
class Solution(object):
    def merge(self, arr1, size1, arr2, size2):
        left = size1 - 1
        right = size2 - 1
        pos = size1 + size2 - 1
        
        while right >= 0:
            if left >= 0 and arr1[left] > arr2[right]:
                arr1[pos] = arr1[left]
                left -= 1
            else:
                arr1[pos] = arr2[right]
                right -= 1
            pos -= 1

        

# Here, I merge two arrays into one sorted array
# I start from the back of both arrays because the biggest numbers will go there 
# I compare the last numbers of both arrays and put the larger one in the last empty spot of arr1
# i keep moving the pointers and repeat until arr2 is fully merged into arr1

#  3.
class Solution(object):
    def intersection(self, arr1, arr2):
        elements = set(arr1)
        result = []
        for value in arr2:
            if value in elements:
                result.append(value)
                elements.remove(value)
        return result

# To find common elements between two arrays, I first store all elements of the first array in a set so I can look them up quickly.
# Then I go through the second array, and if an element is in the set, I add it to the result and remove it from the set to avoid duplicates. 
# At the end, I return the result.
