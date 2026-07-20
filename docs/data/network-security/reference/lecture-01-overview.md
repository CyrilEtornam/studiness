# Lecture 1 — Security Overview & Fundamentals

CPEN 426 — Computer & Network Security, University of Ghana. This lecture introduces the vocabulary and mental model the rest of the course builds on.

## What is security?

Information security is the practice of protecting information and information systems from unauthorized access, use, disclosure, disruption, modification, or destruction.

Four core terms, kept carefully distinct throughout the course:

| Term | Definition |
|---|---|
| Vulnerability | A weakness in a system that could be exploited |
| Threat | A potential danger that could exploit a vulnerability |
| Attack | The actual attempt to exploit a vulnerability |
| Risk | The likelihood of a threat exploiting a vulnerability, combined with the resulting impact |

A system can have a vulnerability with no active threat yet, and a threat with no exploitable vulnerability — the terms describe different stages of the same underlying danger, not synonyms for it.

Two more terms describe *exposure*:

- **Attack vector** — the specific path or means by which an attacker gains access (e.g. a phishing email, an open port, an unpatched library).
- **Attack surface** — the total sum of every possible attack vector into a system. Reducing attack surface (fewer exposed services, less running code, fewer entry points) is a core, general-purpose defensive strategy, because it shrinks the number of vectors available regardless of which specific vulnerability an attacker might target.

## The CIA triad

The foundational model for information security is the **CIA triad**:

- **Confidentiality** — information is not disclosed to unauthorized parties.
- **Integrity** — information is not altered improperly, whether in transit or storage.
- **Availability** — information and systems remain accessible to authorized users when needed.

The course extends this with two further principles, since not every failure fits neatly into C, I, or A:

- **Authenticity** — verifying that data, or a user, really is who/what it claims to be.
- **Accountability** — the ability to trace an action back to the specific party responsible for it.

These two extras matter because they answer genuinely different questions from integrity. Data can be perfectly unaltered (high integrity) but still forged from the very start by an impersonator — an authenticity failure, not an integrity one. Or data can be correctly altered by an authenticated party who later denies having done so — an accountability failure, even though nothing was technically tampered with in an unauthorized way.

**Worked distinctions:**
- A denial-of-service flood that doesn't read or change any data, but blocks legitimate customers from reaching a server, violates **availability**.
- An attacker who intercepts and silently modifies a bank transfer's destination account violates **integrity**.
- Someone who convincingly impersonates another user's identity violates **authenticity**.
- A user who denies performing an action that the system can't conclusively prove they took violates **accountability**.

## Threats and attacks

- **Phishing** — a social-engineering attack that tricks users into revealing credentials or sensitive information, typically via deceptive email or messages. It exploits human trust and judgment, not a technical flaw — which is why patching software alone doesn't stop it; user awareness and verification habits do.
- **Advanced Persistent Threat (APT)** — a prolonged, targeted campaign in which an intruder gains and maintains unauthorized, stealthy access to a network over an extended period, typically to steal data over time rather than cause immediate, visible damage. The "persistent" part is the defining feature.
- **Insider threat** — originates from someone with legitimate authorized access (an employee, contractor, or partner) who misuses that access, whether maliciously or by accident. Insider threats are notoriously hard to defend against because most security controls are built around a *perimeter* — keeping unauthorized outsiders out — and an insider starts already inside that boundary with valid credentials, so perimeter defenses simply don't apply to them.
- **Denial of Service (DoS)** — an attack aimed at making a system or service unavailable to legitimate users, directly targeting the availability leg of the CIA triad.
- **Malware** — malicious software (viruses, worms, trojans, ransomware, spyware) designed to damage, disrupt, or gain unauthorized access to a system.

## The attacker landscape

Attacker capability is often profiled along several dimensions: **motive**, **knowledge**, and **resources**. Two attackers with identical technical skill can pose very different risks depending on what they're after — a financially-motivated criminal typically takes the path of least resistance to any monetizable target, while a well-resourced, targeted adversary (e.g. state-sponsored) will persist against one specific target regardless of difficulty. Profiling motive, not just skill, helps predict attacker behavior and prioritize defenses.

Key attacker-side concepts:

- **Zero-day vulnerability** — a flaw unknown to the vendor (and therefore unpatched) at the time it's discovered or exploited. Since the whole patch/signature-based defense ecosystem depends on a vulnerability being *known*, a zero-day has no targeted countermeasure ready, making it especially dangerous and valuable on exploit markets.
- **Privilege escalation** — exploiting a bug or design flaw to gain access beyond what was originally granted (e.g. regular user → administrator).
- **SQL injection (SQLi)** — occurs when unsanitized user input is concatenated directly into a database query, letting an attacker manipulate the query's own logic (e.g. bypass authentication, dump data).
- **Cross-site scripting (XSS)** — the analogous problem for web output: unsanitized input gets rendered as executable script in a victim's browser.

Both SQLi and XSS share the same root cause: an application trusting unsanitized input.

## Security policy and mechanisms

- **Security policy** — a formal, documented set of rules and practices specifying how an organization manages, protects, and distributes sensitive information. The policy defines the *what* and *why*.
- **Security mechanisms (services)** — the specific technical or procedural controls (encryption, access control, auditing, etc.) implemented to enforce a policy's goals. Mechanisms are the *how*.

Keeping policy and mechanism conceptually separate matters: it lets an organization swap out or upgrade its technical tools over time without rewriting its underlying rules, and lets it audit whether current mechanisms actually satisfy the stated policy.
