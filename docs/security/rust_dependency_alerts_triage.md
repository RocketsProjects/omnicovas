# Rust Dependency Alert Triage — glib and rand

Date: 2026-05-03
Branch: chore/rust-dependency-security-updates

---

## Summary

GitHub Dependabot flagged two packages in `src-tauri/Cargo.lock`:

- **glib** (GHSA-wrw7-89jp-8q8g) — vulnerable version 0.18.5, patched floor 0.20.0
- **rand** (GHSA-cq8v-f236-94qc) — vulnerable version 0.7.3, patched floor 0.8.6

Investigation attempted safe Cargo/Tauri updates to clear both alerts.
Both alerts are upstream/transitive constraints, not OmniCOVAS source-code vulnerabilities.
No `Cargo.toml` or `Cargo.lock` changes were made.
No source changes are recommended at this time.

---

## Advisory Table

| Advisory | Package | Current version | Patched version/floor | Dependency path | Status | Risk context | Next review trigger |
|---|---|---|---|---|---|---|---|
| GHSA-wrw7-89jp-8q8g | glib | 0.18.5 | 0.20.0 | omnicovas → tauri v2.10.3 → gtk v0.18.2 → glib v0.18.5 | Upstream-blocked (GTK-rs constraint) | Linux/BSD-target path only; absent from Windows x86_64-pc-windows-msvc tree | Tauri/wry/tao/gtk-rs release that migrates to glib 0.20+ |
| GHSA-cq8v-f236-94qc | rand | 0.7.3 | 0.8.6 (rand 0.8.6 already present) | rand v0.7.3 → phf_generator v0.8.0 → phf_codegen v0.8.0 → selectors v0.24.0 → kuchikiki v0.8.8-speedreader → tauri-utils v2.8.3 → Tauri stack | Upstream-blocked (kuchikiki mandatory in tauri-utils) | Build-time transitive path through PHF generation, not an OmniCOVAS runtime API usage path | tauri-utils release that removes or gates kuchikiki |

---

## glib — GHSA-wrw7-89jp-8q8g

### Dependency path

```
omnicovas v0.1.0
└── tauri v2.10.3
    └── gtk v0.18.2 (Linux target)
        └── glib v0.18.5   ← vulnerable
```

Full tree (from `cargo tree --target all -i glib`):

```
glib v0.18.5
├── atk v0.18.2
│   └── gtk v0.18.2
│       ├── muda v0.17.2
│       │   └── tauri v2.10.3
│       ├── tao v0.34.8
│       │   └── tauri-runtime-wry v2.10.1
│       ├── tauri v2.10.3
│       ├── tauri-runtime v2.10.1
│       ├── tauri-runtime-wry v2.10.1
│       ├── webkit2gtk v2.0.2
│       └── wry v0.54.4
├── cairo-rs v0.18.5
├── gdk v0.18.2
├── gdk-pixbuf v0.18.5
├── gdkx11 v0.18.2
├── gio v0.18.4
├── pango v0.18.3
└── soup3 v0.5.0
```

### Cargo blocker

`gtk v0.18.2` declares `glib = "^0.18"` in its manifest. Cargo rejects `glib 0.20.0` because it falls outside the `^0.18` semver requirement. No project-level override is possible without also upgrading `gtk` to a version that accepts glib 0.20+.

### Target context

`cargo tree --target x86_64-pc-windows-msvc -i glib` returned **nothing to print** — the Windows MSVC target tree does not include this path. The glib/gtk stack is a Linux/BSD platform dependency. OmniCOVAS is Windows-first.

### Why not fixing now

Fixing requires upstream Tauri (and transitively wry, tao, gtk-rs) to migrate their Linux GTK stack to a glib 0.20+ compatible set of crates. That is not a change OmniCOVAS can make at the project level without breaking the Tauri Linux build.

### Next review trigger

New Tauri / wry / tao / tauri-runtime-wry release that migrates away from gtk-rs 0.18 or explicitly supports glib 0.20+. Check Tauri changelog and `tauri-sys` / `gtk-rs` release notes.

---

## rand — GHSA-cq8v-f236-94qc

### Dependency path

```
rand v0.7.3   ← vulnerable (no 0.7.x patch exists)
└── phf_generator v0.8.0
    └── phf_codegen v0.8.0
        [build-dependencies]
        └── selectors v0.24.0
            └── kuchikiki v0.8.8-speedreader
                └── tauri-utils v2.8.3
                    ├── tauri-build v2.5.6  [build-dep]
                    ├── tauri-codegen v2.5.5
                    ├── tauri-macros v2.5.5
                    └── tauri-plugin v2.5.4  [build-dep]
```

Full tree (from `cargo tree --target all -i rand@0.7.3`): confirmed above.

### Patched rand already present

`rand v0.8.6` is already present in `Cargo.lock` and satisfies all direct and other transitive uses. The problem is the `rand v0.7.3` pin inside `phf_generator 0.8.0`, which has no 0.7.x patch release. Upgrading the `phf_*` crates would require upgrading `selectors`, which would require an upstream change in `kuchikiki`.

### Same-major Tauri experiment result

Bumping `tauri-utils` to v2.9.0 in `Cargo.toml` was tested. `tauri-utils v2.9.0` still includes `kuchikiki` as a mandatory (non-optional) dependency. The `rand v0.7.3` path survives. The experiment was reverted; `Cargo.toml` and `Cargo.lock` are at their original state.

### Risk context

This is a **build-time transitive path** through PHF (perfect hash function) generation code, not an OmniCOVAS runtime API usage path. The `phf_codegen` crate generates compile-time hash tables; `rand` is used only during that generation step, not in the shipped binary's hot path.

### Advisory exploit context

The rand advisory (GHSA-cq8v-f236-94qc) requires specific runtime conditions: `thread_rng` / `rng` usage, logging features enabled, custom logger behavior, and reseeding. This build-time PHF generation path does not match those conditions — PHF generation runs once at compile time, not in OmniCOVAS's runtime.

### Next review trigger

A `tauri-utils` release that removes or feature-gates `kuchikiki`, or an upstream change in `kuchikiki` / `selectors` / `phf_codegen` that no longer requires `rand 0.7.x`.

---

## GitHub Alert Triage Comments

Exact comments Commander can paste into each GitHub Dependabot alert:

### glib — GHSA-wrw7-89jp-8q8g

```
Triage: no safe project-level update is currently available. `glib 0.18.5` is pulled transitively through the Tauri Linux GTK stack (`tauri 2.10.3 -> gtk 0.18.2 -> glib 0.18.5`). Cargo rejects `glib 0.20.0` because `gtk 0.18.2` requires `glib = "^0.18"`. The Windows target does not include this path in `cargo tree --target x86_64-pc-windows-msvc -i glib`. Tracking upstream Tauri/wry/gtk-rs migration to a glib 0.20+ compatible stack.
```

### rand — GHSA-cq8v-f236-94qc

```
Triage: no safe semver-compatible update is currently available. Patched `rand 0.8.6` is already present; the remaining vulnerable `rand 0.7.3` is a build-time transitive path through `phf_generator 0.8.0 -> phf_codegen 0.8.0 -> selectors 0.24.0 -> kuchikiki 0.8.8-speedreader -> tauri-utils`. A same-major Tauri/Tauri-utils update was tested and did not remove the kuchikiki/rand@0.7.3 path. The advisory requires runtime custom logger/thread_rng conditions that do not match this build-time PHF generation path. Tracking upstream tauri-utils/kuchikiki/selectors updates.
```

---

## Recommended GitHub Disposition

### glib

- **Keep open** if Commander wants visible upstream tracking in the Dependabot dashboard.
- **Dismiss as "vulnerable code not used"** or **"tolerable risk"** if Commander accepts:
  - OmniCOVAS is Windows-first; the glib path is absent from the Windows MSVC target tree.
  - The fix is upstream-blocked by the Tauri/gtk-rs ecosystem; no project-level action is available.

### rand

- **Keep open** if Commander wants visible upstream tracking in the Dependabot dashboard.
- **Dismiss as "vulnerable code not used"** or **"tolerable risk"** if Commander accepts:
  - Exposure is confined to a build-time transitive path through PHF generation.
  - The advisory's runtime exploit conditions (custom logger, thread_rng, reseeding) do not apply to this compile-time path.
  - No project-level Cargo update can remove this path without an upstream tauri-utils change.

---

## Investigation Commands Used

```powershell
# Confirm no Cargo changes
git diff -- src-tauri/Cargo.toml src-tauri/Cargo.lock

# glib path across all targets
cargo tree --manifest-path src-tauri/Cargo.toml --target all -i glib

# glib on Windows MSVC only (returned nothing — not present)
cargo tree --manifest-path src-tauri/Cargo.toml --target x86_64-pc-windows-msvc -i glib

# rand 0.7.3 path across all targets
cargo tree --manifest-path src-tauri/Cargo.toml --target all -i rand@0.7.3
```
