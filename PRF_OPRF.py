from hashlib import sha256
from helpers import (
    p, g, modinv, H1, H2, random_scalar,random_scalar_coprime_to_phi
)



def run_setup():
    try:
        open("server_key.txt", "x").write(str(random_scalar()))
        print("\nGenerated new server key.\n")
    except FileExistsError:
        print("\nServer key already exists.\n")
        pass



def simple_prf_eval(key: int, x: bytes) -> bytes:
    """Server-side PRF: PRF_k(x) = SHA256(k || x)."""
    return sha256(key.to_bytes(32, 'big') + x).digest()
        


def prf_local(x: bytes):
    # Read master key
    with open("server_key.txt") as f:
        k = int(f.read())

    y = simple_prf_eval(k, x)

    return y.hex()



def oprf_local(x: bytes):
    # Read master key
    with open("server_key.txt") as f:
        k = int(f.read())

    r = random_scalar_coprime_to_phi(phi = p - 1)

    H = H1(x)
    a = pow(H, r, p)
    b = pow(a, k, p)

    r_inv = modinv(r, p - 1)
    c = pow(b, r_inv, p)

    y = H2(x, c)

    return y



if __name__ == "__main__":
    msg = b"carol@example.com"
    y1 = prf_local(msg)
    y2 = oprf_local(msg)
    print("PRF(x)  =", y1)
    print("OPRF(x) =", y2)
    print("Match?  ", y1 == y2)
