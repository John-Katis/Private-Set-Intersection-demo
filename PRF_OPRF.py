"""
    In this file, you will have to write code implementing a PRF and an OPRF. (see README)

    Your task is to evaluate both with a given key from run_setup(). Both schemes should
    apply the key on the input in the way specified by each protocol.

    What is more, the OPRF function that you will build here will be a critical component
    in the next task: Building a protocol for PSI.
"""


from hashlib import sha256
from helpers import (
    p, g, modinv, H1, H2, 
    random_scalar, random_scalar_coprime_to_phi,
    load_server_key
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
    # use sha256(k + x).digest() to get bytes
    # TODO
    eval_result = None
    return eval_result



def prf_local(x: bytes):
    k = load_server_key()

    # Eval prf - call the function above
    # TODO
    y = None

    return y # or y.hex()



def oprf_local(x: bytes):
    k = load_server_key()

    # Derive randomness, coprime to Phi = p - 1
    # TODO

    # User computes a = H1(x)^r
    # TODO

    # Server computes b = a^k
    # TODO

    # User inverts r and computes c
    # TODO

    # User output y = H2(x, c)
    # TODO
    y = None

    return y



if __name__ == "__main__":
    run_setup()
    msg = b"carol@example.com"
    y1 = prf_local(msg)
    y2 = oprf_local(msg)
    print("PRF(x)  =", y1)
    print("OPRF(x) =", y2)
    print("Match?  ", y1 == y2)
