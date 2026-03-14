# PSI with Simple ORPF demo

### Contents

1. [PRF scheme](#prf-scheme)
2. [OPRF scheme](#oprf-scheme)
3. [PSI scheme](#psi)

This repository contains 3 files, 2 of which define tasks to be completed in order to implement:

1. `PRF_OPRF.py`: a simple PRF and OPRF function
2. `PSI.py`: a PSI protocol using the given OPRF function

The goal of the PSI protocol that we build is to match Alice's (the user) passwords, with a list of passwords that are known to be broken for a given service provider (e.g., Google, Meta, AWS etc.). Therefore, both Alice and the Service provider would like to keep their sets secret.

Your task will be to implement first a PRF and OPRF. This will showcase the concrete differences between the two. Based on the OPRF function that you will write, you will then move on to building the PSI protocol.

All inputs are given and hash function outputs - OPRF inputs are harmonized through the `make_public_hashes` function in `PSI.py`.

Below, we provide clarification on each protocol:

## PRF scheme

```
Server holds key k

User holds input x

PRF = H(x + k), where H is a hash function
```

## OPRF scheme

![2 hash OPRF](./images/2%20hash%20OPRF.png)

## PSI

The proposed protocol is defined originally in [this slide deck](https://csrc.nist.gov/CSRC/media//Projects/pec/documents/stppa-02-PSI-rosulek.pdf), created by Mike Rosulek for the NIST STPPA workshop. The specific protocol is given in slides 44-56. Below, an overview of the protocol is given.

In `PSI.py` the steps of the protocol are analytically provided as 'skeleton code' that you have to fill in and make the protocol execute correctly.

```
Public: h1, h2: bytes -> 32B; bins m
Input:  X (Alice), Y (Bob)

1) Alice places each x into bin h1 or h2

2) Bob places each y into both bins h1 and h2

3) Apply OPRF F() in each bin:
3.1) Alice learns F(h1(x)) or F(h2(x)) based on step 1
3.2) Bob learns all F() evaluations for both bins

4) Bob sends his list to Alice

5) Alice checks for matching values and outputs the intersection
```