def squares(n, m):
    def gcd(a ,b):
        while b != 0:
            a, b = b, a % b
        return a
    gcd = gcd(n, m)
    n = n // gcd
    m = m // gcd
    return n * m

print(squares(6, 10))