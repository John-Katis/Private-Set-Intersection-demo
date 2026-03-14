from hashlib import sha256
from typing import List, Tuple, Dict, Callable, Set
# NOTE: oprf_local is also a task
# NOTE: please complete that before coding here
from PRF_OPRF import run_setup, oprf_local
import time



# Public hash functions h1, h2
def make_public_hashes(m: int) -> Tuple[
    Callable[[bytes], bytes], Callable[[bytes], bytes]
]:
    """
    Returns a 2-tuple:
      - h1_val : bytes -> 32-byte digest (prefix: h1:val|)
      - h2_val : bytes -> 32-byte digest (prefix: h2:val|)
    The output type is compatible with oprf_local() input type.
    """

    def h_val(tag: bytes, x: bytes) -> bytes:
        return sha256(tag + x).digest()


    h1_val = lambda x: h_val(b"h1:val|", x)
    h2_val = lambda x: h_val(b"h2:val|", x)

    return h1_val, h2_val



def Alice_placement(
    X: List[bytes], m_bins: int = 128
) -> Tuple[Dict[int, bytes], Callable[[bytes], bytes], Callable[[bytes], bytes]]:
    """
    Returns:
      - bins_a: dict bin_idx -> list of (x, v) where v is the HASHED VALUE used as OPRF input:
                v = h1_val(x) if placed by h1_bin, else v = h2_val(x)
      - h1_val, h2_val : the public hash functions used
    Strategy:
      1) i1 = h1_val(x); if 'unused' reserve i1 for the first item hitting it, place h1_val(x)
      2) else i2 = h1_val(x); if 'unused' reserve i2, place h2_val(x)
      3) else fallback: still use i1 and h1_val(x) (allow multiple same hash values for demo)
    """
    h1_val, h2_val = make_public_hashes(m_bins)
    used: Set[int] = set()
    bins_a: Dict[int, bytes] = {}

    # Run strategy - iteration over inputs
    # TODO

        # Check first bin
        # TODO
            # Place if possible, update used
            # TODO
        
        # Check second bin
        # TODO
            # Place if possible, update used
            # TODO

        # Fallback: allow multiple same hash values
        # TODO

    return bins_a, h1_val, h2_val



def Provider_placement(
    Y: List[bytes],
    h1_val: Callable[[bytes], bytes],
    h2_val: Callable[[bytes], bytes]
) -> List[bytes]:
    """
    Returns bins_b_inputs: List 
      -> contains all of Bobs items hashed with both h1 and h2
    These v values are the inputs that Bob will run OPRF on.
    """
    bins_b_inputs = []

    # Run 'Bob' strategy - hash all inputs with both functions
    # TODO

    return bins_b_inputs



def psi_oprf_intersection(X: List[bytes], Y: List[bytes], m_bins: int = 128) -> List[bytes]:
    """
    Compute X ∩ Y with OPRF applied AFTER deriving the per-hash value:
      - Alice places x using h1_val/h2_val and computes v = h1_val(x) or v = h2_val(x),
        then computes OPRF(v) and stores per-bin.
      - Broken passwords provider inserts y into BOTH bins and computes OPRF(h1_val(y)) and
        OPRF(h2_val(y)) into the corresponding bins.
      - Alice matches per-bin on OPRF outputs. Outputs the intersection
    """
    # Ensure master key exists (created once)
    run_setup()

    # 1) Alice placement -> per-bin list of (x, v) where v is the OPRF input
    # TODO

    # 2) Broken passwords provider placement -> per-bin list of v inputs for OPRF
    # TODO

    # 3) Evaluate OPRF on all v's
    # 3.1) Alice: per-bin list of (x, OPRF(v))
    # TODO

    # 3.2) Broken passwords provider: per-bin set of OPRF(v) values for quick membership tests
    # TODO
    
    # 4) Compare per bin
    # TODO
    intersection = []

    return intersection



if __name__ == "__main__":
    # Example sets (bytes)
    X = [b"password123", b"123password", b"xz.!ppa1023"]
    Y = [b"password123", b"123password", b"123456", b"user.123", b"user.userson", b"user.mail@mail.com_pwd"]

    start = time.time()
    inter = psi_oprf_intersection(X, Y, m_bins=64)
    end = time.time()
    
    print(f"Alice's passwords (X):      {X}")
    print(f"Compromised passwords (Y):  {Y}")
    print("\nX \u2229 Y =", [x.decode() for x in inter], F"  found in {end-start} sec\n\n")