"""
n = 1
m = (n**2 + n + 41) ** (1/2)
print (m)
"""

"""
n = 2
m = (n**2 + n + 41) ** (1/2) 
for n in range(2,1000000):
    if int(m) == m:
        break
print (m)
"""

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True

def euler_conjecture():
    for n in range(1, 100):
        value = n**2 + n + 41
        if not is_prime(value):
            print(f"Counterexample n = {n}, value = {value} is not prime.")

euler_conjecture()