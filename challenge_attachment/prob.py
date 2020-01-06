from Crypto.Util.number import *
from secret import *

m = bytes_to_long(flag)
p = getPrime(2048)
q = getPrime(2048)
r = inverse(pow(p, 3), q)
s = (pow(p, 2, p * q) - pow(q, 0x10001, p * q)) % (p * q)
e = 0x10001
n = p * q
assert(m < n)
c = (pow(r * m, e, n) * inverse(s, n)) % n
c = pow(c, 2, n)

open("pub.key", "w").writelines(map(lambda x: x + "\n", map(str, [r, s, e, n])))
open("flag.enc", "w").write(str(c))
