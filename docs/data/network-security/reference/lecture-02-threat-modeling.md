# Lecture 2 — Threat Modeling & Security Policy

CPEN 426 — Computer & Network Security. This lecture covers the structured process of finding threats *before* they're exploited, and how to size and prioritize the risks they represent.

## What is threat modeling?

Threat modeling is a structured process for identifying, understanding, and addressing potential threats to a system — ideally *before or during* its design, not just after deployment. Doing it early is what makes it a proactive rather than reactive practice.

### The threat modeling process (5 steps)

1. **Define objectives and scope** — decide what asset or system is being analyzed and what the analysis is meant to achieve. Without a defined scope, none of the later steps have a boundary to work within.
2. **Build a system diagram** — a Data Flow Diagram (DFD) or Process Flow Diagram (PFD) that visualizes how data moves through the system and where trust boundaries lie. This diagram becomes the map that later steps (like STRIDE) are systematically applied against.
3. **Identify threats** — walk through the diagram's elements (processes, data flows, trust boundaries) and enumerate what could go wrong at each one, typically using a framework like STRIDE (below).
4. **Assess risk and mitigate** — for each identified threat, decide how significant it is and how to respond (fix, mitigate, transfer, or accept).
5. **Validate and iterate** — revisit the model as the system evolves. A threat model is a snapshot of a design at a point in time; as soon as the system changes (new feature, new integration, new data flow), the original model can miss genuinely new attack surface. Threat modeling should be a living process, not a one-off document.

## STRIDE

STRIDE is a threat-categorization framework with six categories, each mapping to the violation of one specific security property from Lecture 1:

| Letter | Category | Property threatened |
|---|---|---|
| S | Spoofing | Authenticity |
| T | Tampering | Integrity |
| R | Repudiation | Accountability |
| I | Information disclosure | Confidentiality |
| D | Denial of service | Availability |
| E | Elevation of privilege | Authorization |

Because each letter corresponds to a distinct security property, working through all six against every element of a system diagram becomes a structured, repeatable checklist — rather than relying on unstructured brainstorming, the modeler is systematically prompted to consider every category of harm at every point in the system.

**Worked example (IoT smart door lock):** After mapping the lock's assets, actors, and data flows (e.g. the wireless link between a mobile app and the lock), STRIDE is applied per element. "Spoofing the mobile app's identity to the lock over the wireless channel" is a much more useful finding than a vague "the lock might get hacked" — it points directly at a concrete mitigation (mutual authentication/pairing), because it's tied to a specific data flow rather than being a generic worry.

## Other threat modeling methods

STRIDE isn't the only method in use:

- **PASTA** (Process for Attack Simulation and Threat Analysis) — risk-centric and attacker-focused, simulating real attack scenarios and tying them to business impact across the full attack lifecycle. Where STRIDE emphasizes systematic design-level coverage, PASTA emphasizes attacker realism and business risk.
- **TRIKE** — a risk-based threat modeling methodology.
- **VAST** (Visual, Agile, and Simple Threat modeling) — designed to scale across large organizations and integrate with agile development.
- **Attack trees** — represent an attacker's ultimate goal as a root node, with child nodes branching into the concrete sub-steps (combined via AND/OR logic) that could achieve it. This decomposition makes the many different routes to the same goal explicit and comparable, which is exactly what lets defenders spot a single mitigation that closes off several branches at once.
- **CVSS** (Common Vulnerability Scoring System) — a standardized scoring system for rating vulnerability severity, often used alongside any of the above methods to prioritize which threats get addressed first.

## Security risk assessment

Once threats are identified, they need to be sized so effort can be prioritized.

**Annualized Loss Expectancy (ALE):**

> ALE = SLE × ARO

- **SLE (Single Loss Expectancy)** — the expected cost of one incident.
- **ARO (Annualized Rate of Occurrence)** — the expected number of incidents per year (can be a fraction, e.g. 0.4 = roughly once every 2.5 years).

ALE converts an irregular, occasional loss into a single comparable yearly figure — which is what lets it be weighed directly against the annual cost of a proposed security control. If a $15,000/year control fully prevents a risk with an ALE of $20,000, it's a net financial win on a pure cost basis (real decisions also weigh non-financial factors like reputational damage).

**Worked example:** A ransomware scenario with SLE = $50,000 and ARO = 0.4 gives ALE = $50,000 × 0.4 = **$20,000/year**.

**Residual risk** — the risk that remains after mitigation controls have been applied. No realistic set of controls reduces risk to exactly zero; organizations explicitly decide how much residual risk they're willing to accept as part of any risk management process. NIST publishes formal risk assessment guidelines that many organizations follow for structuring this process.

## Security policy

A **security policy** is the formal, documented set of rules an organization follows to manage, protect, and distribute sensitive information — separate from (and enforced by) the specific technical mechanisms in place. See Lecture 1's closing section for how policy and mechanism relate.
