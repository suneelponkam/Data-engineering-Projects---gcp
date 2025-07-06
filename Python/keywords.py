


 #try, except, and yield in Python. Let me break these down real quick and then show you how they work together

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Oops! {e}")


#o/p: Oops! division by zero


def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for num in count_up_to(3):
    print(num)

#o/p: 
# 1
# 2
# 3
