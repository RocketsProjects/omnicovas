# Security Policy

## Our commitment

OmniCOVAS handles sensitive local commander context: Elite Dangerous journal data, companion JSON snapshots, settings, API keys, optional authenticated provider data, and future shared-operation state. Security is therefore part of the project architecture, not an afterthought.

The project’s security posture is defined by the current authority family:

- `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_Human_Reference.txt`
- `docs/internal/blueprints/OmniCOVAS_Master_Blueprint_v5_0_AI_Reference.txt`
- `docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_Human_Reference.txt`
- `docs/internal/blueprints/OmniCOVAS_Backend_Blueprint_v1_0_AI_Reference.txt`
- `docs/internal/blueprints/OmniCOVAS_Source_Capability_Routing_Reference_v1.txt`
- `docs/internal/blueprints/OmniCOVAS_Compliance_Matrix_v4_1.txt`
- `docs/decisions/0003-ui-safe-rendering.md`

## Reporting a vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

To report a security issue:

1. Go to the repository’s **Security** tab.
2. Choose **Report a vulnerability** to use GitHub Private Vulnerability Reporting.
3. Include, where possible:
   - a clear description of the issue;
   - steps to reproduce;
   - affected commit, version, or branch;
   - expected impact;
   - proof-of-concept details you are comfortable sharing;
   - whether the issue may expose secrets, commander data, local files, external-provider credentials, bridge access, or UI execution paths.

## Response timeline

OmniCOVAS is a zero-budget volunteer project, but security reports are treated seriously.

- **Acknowledgment:** target within 72 hours.
- **Initial assessment:** target within 7 days.
- **Fix development:** as fast as responsibly possible; complex issues may take longer.
- **Coordinated disclosure:** public details are coordinated with the reporter when possible.

## Recognition

Responsible disclosure is appreciated. Reporters may be credited in release notes or a security acknowledgments section unless they prefer to remain anonymous.

OmniCOVAS cannot offer cash bounties.

## Security commitments

OmniCOVAS is designed around these commitments:

- **Local-first by default.** Commander journal data, companion JSON snapshots, state, settings, logs, and local cache remain local unless the commander explicitly enables an outbound flow.
- **No maintainer telemetry.** OmniCOVAS does not report analytics, usage telemetry, or commander data back to project maintainers.
- **Secrets are encrypted at rest.** API keys and provider secrets are stored through the Windows DPAPI-backed vault.
- **Secrets are redacted before logging.** Logs must not contain API keys, tokens, secrets, or credential payloads.
- **Outbound data is opt-in.** External requests require explicit commander control and must be visible in Activity Log.
- **Source routing is bounded.** External providers are used only for supported facts, within respectful project request budgets, with cache/batch behavior before calls.
- **AI is not a fact source.** AI may draft, summarize, classify intent, or prepare a plan; it may not invent facts or bypass source routing.
- **NullProvider must work.** Core functionality must continue when AI is disabled.
- **Confirmation Gate is mandatory.** Protected actions require commander confirmation and audit records.
- **No unattended automation.** OmniCOVAS must not bot, farm, manipulate game memory, bypass the game client, or perform direct AI in-game actions.
- **UI rendering is defensive.** Telemetry, provider data, user input, logs, and WebSocket payloads must not be rendered through unsafe dynamic HTML. Follow ADR 0003.
- **Activity Log is the proof layer.** Meaningful state changes, source chains, external requests, AI drafts, gate decisions, blocked requests, exports, deletes, and diagnostics must be auditable.

## In scope

Security reports are welcome for:

- OmniCOVAS source code in this repository;
- the Python backend;
- the Tauri desktop shell;
- the FastAPI bridge and WebSocket event stream;
- local file watchers and parsers;
- Activity Log, source chain, and redaction behavior;
- Windows DPAPI vault behavior;
- settings/privacy/source toggles;
- external request routing, consent, authentication, cache, and rate handling;
- AI provider abstraction and NullProvider behavior;
- Confirmation Gate behavior;
- UI safe rendering, overlay, and bridge-to-renderer paths;
- build, dependency, packaging, signing, and release pipeline behavior;
- documentation issues that could cause unsafe implementation.

## Out of scope

The following are generally out of scope for this repository:

- vulnerabilities in Elite Dangerous itself;
- vulnerabilities in third-party providers or services;
- vulnerabilities in operating-system components unrelated to OmniCOVAS use;
- vulnerabilities in user-installed third-party tools or plugins that OmniCOVAS does not bundle;
- social engineering against maintainers or users;
- denial-of-service tests against external community providers.

If an issue crosses a boundary, report it privately and identify the affected project or provider where possible.

## Handling external-provider issues

If a report involves an external API or community provider, OmniCOVAS will:

1. avoid public disclosure until the issue is understood;
2. disable, block, or gate the affected OmniCOVAS integration if needed;
3. coordinate with the provider when appropriate;
4. preserve Activity Log visibility and commander-facing fallback wording;
5. avoid workarounds that violate provider terms, privacy rules, or respectful request budgets.

## Safe-rendering rule

For UI security, follow `docs/decisions/0003-ui-safe-rendering.md`:

- Prefer `document.createElement` and `textContent` for dynamic values.
- Use project-approved escaping only where explicitly allowed.
- Reject unsafe dynamic `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `new Function`, or string-based timers for untrusted data.

## Security review expectations

Security-sensitive pull requests should identify:

- affected data flows;
- new or changed outbound behavior;
- secret-handling behavior;
- Activity Log coverage;
- Confirmation Gate coverage;
- privacy/default state;
- UI rendering posture;
- verification commands run.

Thank you for helping keep OmniCOVAS and its commanders safe.


---

Documentation router: use `docs/internal/blueprints/OmniCOVAS_Index.md` and `docs/internal/blueprints/OmniCOVAS_Index_AI_Reference.md` to locate the current v5.0 authority documents. The Index is a router only; it does not override the owning authority files.
