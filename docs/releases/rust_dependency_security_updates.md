# Security: Rust Dependency Alert Triage — glib and rand

Date: 2026-05-03
Branch: chore/rust-dependency-security-updates

---

## Summary

GitHub Dependabot flagged two Rust packages in `src-tauri/Cargo.lock`:

- **glib 0.18.5** — advisory GHSA-wrw7-89jp-8q8g (patched floor: glib 0.20.0)
- **rand 0.7.3** — advisory GHSA-cq8v-f236-94qc (patched floor: rand 0.8.6)

**No dependency changes were made.** Both alerts are blocked by upstream Tauri/transitive ecosystem constraints that cannot be resolved at the OmniCOVAS project level.

Full investigation detail, dependency paths, and GitHub triage comments:
→ [`docs/security/rust_dependency_alerts_triage.md`](../security/rust_dependency_alerts_triage.md)

---

## Status

| Package | Alert | Outcome |
|---|---|---|
| glib 0.18.5 | GHSA-wrw7-89jp-8q8g | Upstream-blocked. gtk v0.18.2 requires `glib = "^0.18"`; upgrade impossible without gtk-rs ecosystem update. Windows target unaffected. |
| rand 0.7.3 | GHSA-cq8v-f236-94qc | Upstream-blocked. rand 0.7.3 pinned by phf_generator 0.8.0 via kuchikiki in tauri-utils. Build-time path only; runtime exploit conditions do not apply. |

---

## Next Review Triggers

- **glib**: New Tauri / wry / tao / gtk-rs release that migrates to a glib 0.20+ compatible stack.
- **rand**: tauri-utils release that removes or feature-gates kuchikiki, or upstream kuchikiki/selectors/phf_codegen update.
