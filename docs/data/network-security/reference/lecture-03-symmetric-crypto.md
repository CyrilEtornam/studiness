# Lecture 3 — Symmetric-Key Cryptography (AES)

CPEN 426 — Computer & Network Security. This lecture moves from *finding* threats to *defending* against them with cryptography, starting with symmetric (shared-key) systems.

## Terminology

- **Plaintext** — the original, readable message.
- **Ciphertext** — the scrambled, unreadable result after encryption.
- **Cipher** — the algorithm that transforms plaintext to ciphertext and back.
- **Key** — the secret parameter that controls exactly how a cipher transforms the message.
- **Cryptanalysis** — the study of methods for breaking cryptographic systems, i.e. recovering plaintext or the key without authorized access.
- **Steganography vs. cryptography** — cryptography scrambles a message's content but doesn't hide that a message exists; steganography hides the very *existence* of a message (e.g. inside an image). An encrypted message is visibly suspicious ("something secret is being sent"), whereas a well-hidden steganographic message can pass unnoticed entirely — which is why the two are sometimes combined for layered protection.

## A brief evolution of cryptography

| Era | Milestone |
|---|---|
| ~50 BC | Caesar cipher — earliest known encryption algorithm, used by Julius Caesar for military affairs |
| WWII | Enigma — a rotor-based mechanical cipher device used by Germany |
| 1978 | DES and RSA both emerge — the computer/formal-analysis era, and the arrival of public-key cryptography |
| 2001 | AES published, eventually replacing DES |
| Today | Quantum cryptography is the current research frontier |

Each stage solved a real limitation of what came before it: mechanization scaled substitution complexity beyond hand ciphers, computerization enabled formally-analyzed block ciphers, and public-key cryptography (RSA, covered in Lecture 4) solved the fundamental problem symmetric-only schemes never addressed — how to securely share a secret key in the first place.

## Classical ciphers

The **Caesar cipher** is a monoalphabetic substitution cipher — every plaintext letter always maps to the same ciphertext letter throughout a message. Mathematically, with letters mapped to numeric values 0–25:

> Encryption: **c = E(p,k) = (p + k) mod 26**
> Decryption: **p = D(c,k) = (c − k) mod 26**

where *k* is the shift key (the classic "Caesar shift" uses k=3).

**Worked example:** encrypting "howdy" with key k=5 → numeric plaintext (7,14,22,3,24) → ciphertext (12,19,1,8,3) → "MTBID".

**Why it's weak, despite a huge key space:** a full monoalphabetic substitution has 26! ≈ 4×10²⁶ possible keys — far too many to brute-force. But brute force isn't the only attack. Because the mapping never changes, the ciphertext's letter-frequency distribution still mirrors the underlying language's natural frequency distribution (e.g. "e" is common in English) — an analyst can match frequency patterns to recover the mapping directly, sidestepping the huge key space entirely. This is **frequency analysis**, and it's the fundamental weakness of any monoalphabetic cipher.

A **polyalphabetic cipher** improves on this by changing the substitution mapping as encryption proceeds, so the same plaintext letter no longer always produces the same ciphertext letter — flattening out the frequency signature that made monoalphabetic ciphers crackable.

## Stream ciphers vs. block ciphers

Every modern encryption algorithm transforms plaintext into ciphertext using one of two structural approaches:

**Stream ciphers** encrypt one bit (or byte) at a time, combining each plaintext bit with a corresponding bit of a pseudorandom key stream — typically via **XOR**.

> Encryption: yᵢ = xᵢ ⊕ sᵢ  Decryption: xᵢ = yᵢ ⊕ sᵢ

XOR is its own inverse — (x ⊕ s) ⊕ s = x — which is exactly why the same operation, with the same key stream, works for both encryption and decryption.

**Worked example:** plaintext bits x = 1000001 (ASCII 'A'), key stream s = 0101100 → ciphertext y = x⊕s = **1101101**. The receiver recovers x by XORing y with the same key stream s again.

**Block ciphers** divide the plaintext into fixed-size blocks and encrypt each block as a unit. Every bit of ciphertext in a block depends on every bit of plaintext in that same block — this whole-block interdependency is what produces the **avalanche effect**: a single changed input bit should scramble roughly half the output bits. Common fixed block sizes: 64 bits (DES/3DES), 128 bits (AES).

A naive block cipher has an obvious weakness: identical plaintext blocks always produce identical ciphertext blocks, leaking structural information about the message. This is exactly the problem NIST's *modes of encryption* (below) exist to solve.

### Confusion, diffusion, and the S-P network

Block ciphers are built from alternating rounds of **substitution** and **permutation** (an "S-P network"):

- **Substitution** — a non-linear operation mixing key bits with plaintext bits, producing the **confusion** property (making the relationship between key/plaintext and ciphertext as complex as possible).
- **Permutation** — a linear operation that spreads/scrambles bit positions, producing the **diffusion** property (dissipating redundancy so a local change spreads across the whole block).

An **S-box** (substitution box) performs the substitution using a lookup table; changing one input bit should change about half the output bits. A **P-box** (permutation box) takes the S-box's output and spreads it so the output bits of any one S-box feed into as many different S-boxes as possible in the next round.

Design tradeoffs for any block cipher: larger **block size**, larger **key size**, and more **rounds** all improve security but slow the cipher down; a more complex **sub-key generation algorithm** and **round function** likewise trade analysis-resistance for speed.

## AES (Advanced Encryption Standard)

AES was published in 2001 to replace DES. NIST issued a public call for new encryption algorithms in 1997 (after DES was broken by brute force); 15 candidates were narrowed to 5 finalists — **MARS, RC6, Rijndael, Serpent, and Twofish** — before NIST selected **Rijndael** (created by Vincent Rijmen and Joan Daemen) as the winner, balancing speed, security margin, and flexibility. AES was issued as the FIPS PUB 197 standard.

NIST's stated requirements: a private-key symmetric block cipher, key lengths of 128/192/256 bits, a 128-bit plaintext block, stronger and faster than 3DES, implementable on smart cards, with an active life of 20–30+ years.

**Key sizes and rounds:**

| Variant | Key length (words) | Block size (words) | Rounds |
|---|---|---|---|
| AES-128 | 4 (128 bits) | 4 (128 bits) | 10 |
| AES-192 | 6 (192 bits) | 4 (128 bits) | 12 |
| AES-256 | 8 (256 bits) | 4 (128 bits) | 14 |

AES processes plaintext as a 4×4 matrix of bytes (the **state**), and applies four functions in each round (except the last, which skips MixColumns):

1. **SubBytes** — non-linear substitution: each byte is replaced via a 16×16 lookup table (the S-box, itself generated from Galois Field arithmetic). E.g. hex byte `{68}` is replaced by looking up row 6, column 8 of the S-box.
2. **ShiftRows** — a permutation/transposition step: row 0 of the state is left unchanged; rows 1, 2, 3 undergo a circular left shift of 1, 2, and 3 bytes respectively. This spreads bytes across different columns — necessary for diffusion, since SubBytes alone only transforms bytes in place.
3. **MixColumns** — a diffusion step using arithmetic over the Galois Field GF(2⁸): each column of 4 bytes is treated as a polynomial and transformed via finite-field matrix multiplication (AES uses the irreducible polynomial x⁸+x⁴+x³+x+1, i.e. `{11b}`). Example: `{02}•{87} mod {11b} = {15}`.
4. **AddRoundKey** — a bitwise XOR between the state and a round subkey derived from the main key via the key schedule. This is the **only** step that actually incorporates the secret key — which is exactly why it must run at the start (round 0) and end of every subsequent round: SubBytes/ShiftRows/MixColumns are all fixed, public, key-independent transforms that anyone can compute or invert without the key, so AddRoundKey is what ties every round's output to a genuinely secret value.

Additional supporting operations: **KeyExpansion** derives all the round subkeys from the original cipher key via the AES key schedule (AES needs a separate 128-bit round-key block per round, plus one more for the initial round). Decryption runs the inverse operations (`InvSubBytes`, `InvShiftRows`, `InvMixColumns`) in reverse order.

## Modes of encryption

Modes solve the block-cipher pattern-leakage problem described above. NIST defines five modes, usable with any block cipher (DES, 3DES, AES):

**ECB (Electronic Code Book)** — the simplest mode: each block is encrypted independently with the same key, Cᵢ = E_K1(Pᵢ). *Advantage:* good for a single, small, standalone block (e.g. wrapping one symmetric key) where there's no sequence for a pattern to appear in; blocks can be shuffled/inserted without affecting others. *Limitation:* identical plaintext blocks always produce identical ciphertext blocks — a serious weakness for any message with repeating structure.

**CBC (Cipher Block Chaining)** — resolves ECB's pattern problem via feedback: each block is XORed with the *previous* ciphertext block before encryption, Cᵢ = E_K1(Pᵢ ⊕ Cᵢ₋₁), with a random **Initialization Vector (IV)** standing in for C₋₁ on the very first block. Because each block's output now depends on everything before it (an avalanche-like chaining effect), identical plaintext blocks no longer produce identical ciphertext. The IV must be unique per message under a given key — reusing it makes the first blocks of two messages directly comparable, leaking whether they start with the same plaintext. A change to any block affects all subsequent ciphertext blocks (making rearrangement/tampering evident), but this also makes CBC inherently sequential.

**CFB (Cipher Feedback)** and **OFB (Output Feedback)** — block-cipher modes that behave like stream ciphers, both using feedback mechanisms from previous steps.

**CTR (Counter mode)** — a newer mode, a variant of OFB, but encrypts a **counter value** rather than any feedback value: Cᵢ = Pᵢ ⊕ E_K1(counter_i), where the counter must be different for every block (typically initialized once and incremented by 1 each block). Because each block's keystream is derived purely from its own counter value — independent of any other block — CTR mode supports parallel encryption/decryption and true **random access** to any block, unlike CBC's inherently sequential chain. Used in ATM network security and IPSec. Like OFB, CTR's only hard requirement is that the same key+counter combination is never reused.
