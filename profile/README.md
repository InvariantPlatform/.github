<p align="center">
  <a href="https://invariant-platform.io"><picture><source srcset="https://raw.githubusercontent.com/InvariantPlatform/.github/main/profile/assets/hero.svg" type="image/svg+xml"><img src="https://raw.githubusercontent.com/InvariantPlatform/.github/main/profile/assets/hero.png" width="100%" alt="Invariant Platform: a security posture that proves itself."></picture></a>
</p>

<p align="center">
  <a href="https://invariant-platform.io"><b>invariant-platform.io</b></a> &nbsp;·&nbsp;
  <a href="https://invariant-platform.io/architecture/">Architecture</a> &nbsp;·&nbsp;
  <a href="https://invariant-platform.io/security-posture/">Security posture</a> &nbsp;·&nbsp;
  <a href="https://invariant-platform.io/resiliency/">Resiliency</a> &nbsp;·&nbsp;
  <a href="https://invariant-platform.io/observability/">Observability</a> &nbsp;·&nbsp;
  <a href="https://invariant-platform.io/supply-chain/">Supply chain</a> &nbsp;·&nbsp;
  <a href="https://invariant-platform.io/join/"><b>Join</b></a>
</p>

Invariant Platform is a security-first Kubernetes platform that re-asserts its own security posture every night, from outside itself, and whose only repair is a rebuild from a declaration. Every property it claims is one it checks. The checks ask the cluster's own API and compare the answer with the declaration, not with a list of machines, so they ask the same questions of five nodes as of a thousand.

| **211** | **7** | **2** | **2** |
|:-:|:-:|:-:|:-:|
| decisions<br><sub>numbered, never deleted</sub> | rebuilds<br><sub>from a declaration</sub> | restore drills<br><sub>passed, not assumed</sub> | failure domains<br><sub>and what survives each</sub> |

## Every night, from outside the cluster

A real run, finding included. A failure pages; silence is a written-down gap.

```diff
$ posture-check
+ ok    pod security: 19/19 namespaces enforced
+ ok    network policy: 19 namespaces default-deny
+ ok    admission: 2 policies, 2 enforcing Deny
+ ok    cluster-admin: 5 subjects, all expected
+ ok    flux: 5 kustomizations reconciling
+ ok    supply chain: signature verified, pinned identity
+ ok    credentials: 8 external secrets syncing
+ ok    origin lock: direct bypass refused (000)
+ ok    selinux: both hypervisors enforcing
- FAIL  systemd degraded; unit not on the watch list
```

## Five properties, each one checked

| Property | How it is held |
|---|---|
| **[Architecture](https://invariant-platform.io/architecture/)** | Every component is modelled before it exists. A component the model does not describe fails the build. |
| **[Security posture](https://invariant-platform.io/security-posture/)** | Every invariant, re-asserted nightly from outside the cluster. A failure pages; silence is a written-down gap. |
| **[Resiliency](https://invariant-platform.io/resiliency/)** | No repair path. Anything broken is destroyed and rebuilt from a declaration, and every rebuild is measured. |
| **[Observability](https://invariant-platform.io/observability/)** | Metrics, logs and alert rules live beside the cluster. A monitor inside the thing cannot report it gone. |
| **[Supply chain](https://invariant-platform.io/supply-chain/)** | Nothing reaches the cluster except a signed artifact from one named workflow. A push deploys nothing. |

## How a change reaches the cluster

1. **A reviewed change**: signed commit, pinned versions; tests are a gate.
2. **One named workflow**: builds once and signs keyless, with an SBOM and provenance.
3. **A private registry**: immutable tags; nothing is ever called latest.
4. **The cluster verifies**: the signature against one pinned identity, then applies and prunes.

> [!IMPORTANT]
> There is no path from `git push` to the cluster. A push deploys nothing; only a signed artifact from the one named workflow does.

## The whole story is free. It just isn't anonymous.

Members get a field note from a real incident every Thursday, the decision register (211 decisions in 12 categories, every one numbered, none deleted, released a few each week), the architecture views, and read access to the platform's source. Membership costs nothing: no seat count, no card, and leaving is one click. It opens soon.

**[Membership →](https://invariant-platform.io/join/)**

<sub>Built and run by <a href="https://www.bradpenney.io">Brad Penney</a>.</sub>
