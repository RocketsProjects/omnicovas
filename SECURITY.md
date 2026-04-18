# Security Policy

## Our Commitment

OmniCOVAS takes security seriously. The project handles commander journal files, API keys for third-party services, and optional peer-to-peer squadron telemetry — all of which deserve care.

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

To report a security issue:

1. Go to the [repository's Security tab](https://github.com/RocketsProjects/omnicovas/security)
2. Click **Report a vulnerability** (this uses GitHub's Private Vulnerability Reporting)
3. Provide:
   - A clear description of the vulnerability
   - Steps to reproduce
   - Affected version (commit hash preferred)
   - Potential impact
   - Any proof-of-concept you're comfortable sharing

## Response Timeline

- **Acknowledgment:** within 72 hours
- **Initial assessment:** within 7 days
- **Fix development:** as fast as responsibly possible — complex issues may take longer
- **Coordinated disclosure:** we'll work with you on timing before any public announcement

## Recognition

Responsible disclosure is gratefully acknowledged. Reporters will be credited in the project's security Hall of Fame in release notes, unless you prefer to remain anonymous.

OmniCOVAS is a zero-budget volunteer project and cannot offer cash bounties.

## Security Commitments

OmniCOVAS is built with these security principles enforced in code, not just policy:

- **API keys are never logged.** A redaction processor runs on every log record.
- **API keys are encrypted at rest** using Windows DPAPI, tied to the commander's Windows account.
- **No outbound data without explicit opt-in.** Every external data flow has a toggle, and every default is off.
- **Rate limits are enforced before every external API call**, not retroactively.
- **Data stays local by default.** The commander's journal, state, and logs never leave the machine unless the commander explicitly configures it.
- **No silent operations.** Every API call and action is auditable through the Activity Log.
- **The AI never takes in-game actions.** Every recommendation passes through a Confirmation Gate middleware that cannot be disabled.

See `OmniCOVAS_Master_Blueprint_v4_0.txt` Section 10 (Security Protocol) for the full security architecture.

## Scope

Security reports are welcome for any of the following:

- The OmniCOVAS source code in this repository
- The build and release pipeline (GitHub Actions workflows)
- The contribution process itself

Out of scope:

- Vulnerabilities in third-party dependencies (report those upstream)
- Vulnerabilities in Elite Dangerous itself (report to Frontier Developments)
- Vulnerabilities in user-installed tools such as EDDI or VoiceAttack

Thank you for helping keep OmniCOVAS and its commanders safe.
