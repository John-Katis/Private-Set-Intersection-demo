from hashlib import sha256
import math, secrets

p = 983531983579983617983777983791983819   # 36 digit prime number
g = 5                                      # generator



def random_scalar():
    return secrets.randbelow(p - 2) + 1



def modinv(a, m):
    """Modular inverse using extended Euclid."""
    return pow(a, -1, m)



def H1(x: bytes) -> int:
    """Hash produces an element of Group Gp"""
    h = int.from_bytes(sha256(x).digest(), 'big')
    return pow(g, h, p)



def H2(x: bytes, c: int) -> str:
    """Hash produces a 256 bit string"""
    return sha256(x + c.to_bytes(256, 'big')).hexdigest()



def random_scalar_coprime_to_phi(phi: int) -> int:
    """Sample r uniformly from [0, phi-1] such that gcd(r, phi) = 1."""
    while True:
        r = secrets.randbelow(phi - 1) + 1
        if math.gcd(r, phi) == 1:
            return r



def load_server_key() -> int:
    with open("server_key.txt", "r") as f:
        return int(f.read())
