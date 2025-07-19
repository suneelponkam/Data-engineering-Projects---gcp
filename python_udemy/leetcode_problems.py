two sum :

sol 1: 

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)

        for i in range(0,n-1):
            for j in range(i+1,n):
                if nums[i]+ nums[j] == target:
                   return [i,j]
        return[]

sol2: more efficient :

def twoSum(self, nums: List[int], target: int) -> List[int]:
        new_list={}

        for i,num in enumerate(nums):
            complemet = target - num
            if complemet in new_list:
                return [new_list[complemet],i]
            new_list[num]=i