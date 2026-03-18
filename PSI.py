from hashlib import sha256
from typing import List, Tuple, Dict, Callable, Set
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

    # Run strategy
    for x in X:
        # Check first bin
        i1 = h1_val(x)
        if i1 not in used:
            # Place if possible
            used.add(i1)
            bins_a[x] = h1_val(x)
            continue
        
        # Check second bin
        i2 = h2_val(x)
        if i2 not in used:
            # Place if possible
            used.add(i2)
            bins_a[x] = h2_val(x)
            continue

        # Fallback: allow multiple same hash values
        bins_a[x] = h1_val(x)

    return bins_a, h1_val, h2_val



def Bob_placement(
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

    for y in Y:
        bins_b_inputs.append(h1_val(y))
        bins_b_inputs.append(h2_val(y))

    return bins_b_inputs



def psi_oprf_intersection(X: List[bytes], Y: List[bytes], m_bins: int = 128) -> List[bytes]:
    """
    Compute X ∩ Y with OPRF applied AFTER deriving the per-hash value:
      - Alice places x using h1_val/h2_val and computes v = h1_val(x) or v = h2_val(x),
        then computes OPRF(v) and stores per-bin.
      - Bob inserts y into BOTH bins and computes OPRF(h1_val(y)) and OPRF(h2_val(y))
        into the corresponding bins.
      - Alice matches per-bin on OPRF outputs. Outputs the intersection
    """
    # Ensure master key exists (created once)
    run_setup()

    # 1) Alice placement -> per-bin list of (x, v) where v is the OPRF input
    bins_a, h1_val, h2_val = Alice_placement(X, m_bins=m_bins)

    # 2) Bob placement -> per-bin list of v inputs for OPRF
    bins_b = Bob_placement(Y, h1_val, h2_val)

    # 3) Evaluate OPRF on all v's
    # 3.1) Alice: per-bin list of (x, OPRF(v))
    bins_a_oprf: Dict[int, bytes] = {}
    for key, hash_val in bins_a.items():
        bins_a_oprf[key] = oprf_local(hash_val)

    # 3.2) Bob: per-bin set of OPRF(v) values for quick membership tests
    bins_b_oprf = []
    for hash_val in bins_b:
        bins_b_oprf.append(oprf_local(hash_val))
    
    # 4) Compare per bin
    intersection: List[bytes] = []
    for key, a_oprf_val in bins_a_oprf.items():
        for b_oprf_val in bins_b_oprf:
            if a_oprf_val in b_oprf_val:
                intersection.append(key)

    return intersection



if __name__ == "__main__":
    # Example sets (bytes)
    X = [b"bob", b"carol", b"trent", b"alice", b"dave", b"erin"]
    Y = [b"bob", b"carol", b"trent", b"mallory", b"peggy", b"victor"]

    start = time.time()
    inter = psi_oprf_intersection(X, Y, m_bins=64)
    end = time.time()
    print(f"Alice's set:  {X}")
    print(f"Bob's set:    {Y}")
    print("\nX \u2229 Y =", [x.decode() for x in inter], F"  found in {end-start} sec\n\n")