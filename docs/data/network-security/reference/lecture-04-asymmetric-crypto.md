# Lecture 4 — Asymmetric Cryptography, Hashing & PKI

CPEN 426 — Computer & Network Security. Symmetric ciphers (Lecture 3) need both parties to already share a secret key — this lecture covers how public-key (asymmetric) cryptography solves that bootstrapping problem, plus hashing, signatures, and the trust infrastructure built on top of them.

## RSA

RSA key generation:

1. Select two large prime numbers **p** and **q**, of similar size.
2. Compute **n = p × q** and the totient **φ(n) = (p−1)(q−1)**.
3. Choose a public exponent **k** (also written e) with 1 < k < φ(n) and **gcd(k, φ(n)) = 1** — k and φ(n) must be coprime, because the next step requires computing a modular inverse, which only exists under that condition.
4. Compute the private exponent **d**, the modular multiplicative inverse of k, satisfying **k·d ≡ 1 (mod φ(n))**.
5. Publish **public key PU = (k, n)**; keep **private key PR = (d, p, q)** secret — p and q must never be published, since anyone who recovers them can recompute φ(n) and then d.

Encryption and decryption:

> Encrypt: **C = Mᵏ mod n**  Decrypt: **M = Cᵈ mod n**

**Worked example (from lecture):** p=11, q=3 → n=33, φ(n)=20. Choosing k=3 (coprime with 20), solve 3d ≡ 1 (mod 20): testing d=7 gives 3×7−1=20, exactly divisible by 20, so **d=7**. Public key = (3, 33); private key = (7, 11, 3).

- Encrypting plaintext M=7 (letter H): C = 7³ mod 33 = 343 mod 33 = **13** (letter N).
- Decrypting C=13: M = 13⁷ mod 33 = **7** (letter H) — recovering the original message.

**Why RSA is secure:** the security argument rests entirely on the **integer factorization problem** — given n = p×q for two large primes, recovering p and q from n alone is believed to be computationally infeasible for sufficiently large primes. An attacker who *could* factor n would immediately recompute φ(n) and then the private key d, which is exactly why p and q must be large (not just n being a large number generally — a large n with small factors would be easy to factor).

## Elliptic Curve Cryptography (ECC)

ECC is a modern public-key system based on the algebra of points on an elliptic curve, rather than large-integer factorization:

> **y² = x³ + ax + b (mod p)**, over a finite field, where p is a large prime and a, b are curve coefficients.

**Key generation:** all parties first agree on curve parameters (p, a, b), a **generator point G**, and the curve's order n. Each user picks a random integer as their **private key d**, and computes their **public key Q = d × G** via repeated point operations (**point doubling** — adding a point to itself; **point addition** — adding two distinct points), both defined by specific geometric/algebraic rules on the curve. Recovering d from Q and G is the elliptic-curve discrete logarithm problem, believed computationally infeasible — this is ECC's analogue of RSA's factorization hardness.

**Key exchange (ECDH-style):** Alice computes k = dₐ × Q_B (her private key times Bob's public key); Bob computes k = d_B × Qₐ. Both reduce algebraically to the same point (dₐ×d_B)×G, so they arrive at an identical shared secret without ever transmitting it — the elliptic-curve analogue of Diffie-Hellman. That shared value k can then key a symmetric cipher like AES for the actual message encryption.

**Why ECC matters practically:** it delivers equivalent security to RSA with dramatically smaller keys:

| ECC key size | Equivalent RSA key size |
|---|---|
| 224 bits | 2048 bits |
| 256 bits | 3072 bits |
| 384 bits | 7680 bits |
| 512+ bits | 15360 bits |

Smaller keys mean less computation, memory, and bandwidth — a major advantage for resource-constrained devices (smart cards, IoT sensors, mobile), which is why ECC is popular in those contexts.

## Cryptographic hashing

Hashing transforms plaintext of arbitrary length into a short, fixed-length value (the **hash**, **hash value**, or **message digest**) via a mathematical function. Hashing is much faster to compare/index than the original data, and — critically for security — it should be extremely unlikely for two different inputs to produce the same output.

Security properties a good hash function must satisfy:

- **Pre-image resistance** (one-way property) — given hash output y, it should be infeasible to find any input m such that hash(m) = y. Hash functions lacking this are vulnerable to *preimage attacks*, and this property is exactly what makes password hashing meaningful.
- **Second pre-image resistance** (weak collision resistance) — given a specific input m₁ and its hash, it should be infeasible to find a *different* input m₂ with the same hash. Without this, an attacker could substitute a forged document for a legitimately hashed/signed one.
- **Collision resistance** (strong collision resistance) — it should be infeasible to find *any* two different inputs m₁, m₂ that collide (produce the same hash). This is stronger than second pre-image resistance, because the attacker gets to choose both inputs freely. Because of the birthday paradox, finding *any* collision is roughly √(2ⁿ) work rather than 2ⁿ, so a hash needs roughly double the bit-length to keep collision-resistance as hard as pre-image resistance.
- **Non-malleability** — it should be infeasible to compute hash(m′) from hash(m) for a related message m′, without knowing m itself.
- **Pseudorandomness** — the hash's output should be indistinguishable from a random oracle; any detectable statistical structure could be exploited even without a full break.

**Common algorithms:** MD-5 (Rivest) produces a 128-bit digest via 64 steps (4 rounds of 16); it's now considered weak. SHA-1 (NIST) produces a 160-bit digest and is used more than MD-5, though it too is now deprecated for security-critical use. SHA-256 produces a 256-bit digest and is widely used today.

## Digital signatures

A digital signature serves the role a handwritten signature does — proving origin, authentication, and authority — but works cryptographically.

**Creation (RSA-based):** hash the message to get a digest, then encrypt that digest with the **signer's private key**: **s = Mᵈ mod n**. The signature s is transmitted along with the original message.

**Verification:** the receiver decrypts the signature using the **signer's public key** — **sᵏ mod n = M** — and compares the result against an independently computed hash of the received message. A match confirms both **integrity** (the message wasn't altered) and **authenticity** (it really was signed by the claimed private key). If verification fails, either the message was altered in transit, or it wasn't actually signed by the claimed sender — the check alone can't distinguish which.

Signing the *hash* rather than the raw message is a major performance optimization: public-key operations are expensive, so reducing an arbitrarily large message to a small, fixed-size digest first means the costly asymmetric operation only ever runs on that small digest.

**DSA (Digital Signature Algorithm):** an alternative public-key signature scheme. To sign message m, the signer picks a random integer k (0 < k < q) that must be **unique per signature and destroyed after use — never reused**, then computes r = [gᵏ mod p] mod q and s = k⁻¹·[H(m) + x·r] mod q, sending (r, s) with m. Verification recomputes a value from the public key and checks it matches r.

Reusing k across two DSA signatures is catastrophic: since k appears in both signatures' equations, an attacker with two signatures sharing the same k can solve a system of two equations for two unknowns (k and the private key x) and recover the private key directly — a real-world vulnerability class that has led to actual private key exposures.

## Message Authentication Codes (MAC) and HMAC

A plain hash proves a message wasn't altered, but says nothing about *who* produced it — anyone can compute hash(forged_message) themselves. A **MAC** fixes this by requiring a **shared secret key** in the computation:

> auth_code = MAC(key, message)

Only someone holding the shared key can produce a valid auth_code for a given message, which lets the receiver trust both the message's integrity *and* its origin (that it came from someone possessing the shared key).

**MAC vs. digital signature:** both provide integrity and authenticity, but structurally differently. A signature uses *asymmetric* keys — only the signer holds the private key, but anyone can verify with the public key — which gives it **non-repudiation** (the signer can't credibly deny signing). A MAC uses a single *shared* secret key known to both parties, so it does **not** provide non-repudiation: either party could in principle have generated the same valid MAC.

**HMAC** is a widely used MAC construction combining a hash function with a key-derivation process, commonly built on top of standard hash functions like SHA-256.

## Non-repudiation and Public Key Infrastructure (PKI)

**Non-repudiation** is the cryptographic guarantee that a sender of a message, or a party initiating a transaction, cannot later deny having done so. Mechanisms that provide it: digital signatures, time-stamping (a trusted service recording when an event occurred), and PKI.

**PKI (Public Key Infrastructure)** is the framework that uses digital certificates to manage, distribute, and verify public keys for secure communication and authentication. Public-key cryptography alone solves *how* to encrypt/sign given a key — it doesn't solve the separate problem of trusting *whose* key it actually is, since anyone can generate a keypair and claim any identity. PKI solves this trust problem via:

- **Certificate Authorities (CAs)** — trusted entities that verify identity requests (via a certificate signing request) and issue digital certificates.
- **Digital certificates** — documents that bind a public key to a specific, verified entity (user, device, or service).
- **Public/private keys** — public keys are freely shared for encryption/verification; private keys are kept secret for decryption/signing.
- **Encryption and digital signatures** — the actual cryptographic services PKI enables once identity is bound to a key.
- **Hardware, software, policies, and procedures** — the operational layer managing certificate creation, storage, distribution, and revocation.

Without a trusted third party vouching for the public-key-to-identity binding, an attacker could simply publish their own public key while falsely claiming to be a legitimate party (e.g. "your bank"). The CA's signed certificate is exactly what lets a stranger verify that binding — and, by extension, is what makes a signature verified against a certificate meaningfully traceable back to a real, verified party for non-repudiation purposes.
