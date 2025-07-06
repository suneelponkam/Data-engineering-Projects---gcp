# Problem 1: Find the sum of all the multiples of 3 and 5 that are

for i in range (1,101):
    if i % 3 == 0 and i % 5 == 0:
        print("fizzbuzz")
    if i % 3 == 0:
        print("fizz")
    if i % 5 == 0:
        print("buzz")
    else:
        print(i)


#problem 2: palindrome

def is_palindrome(s):
    s = s.lower()  # Convert to lowercase
    return s == s[::-1]  # Compare with reversed string

# Test cases
print(is_palindrome("madam"))      # True
print(is_palindrome("hello"))      # False
print(is_palindrome("Level"))      # True

#s[start:stop:step]
#So s[::-1] means:
#Start from the end (-1 step = go backward)
#Go all the way to the beginning
#Return a new string that is the reverse of s
