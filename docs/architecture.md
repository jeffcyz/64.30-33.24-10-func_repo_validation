# ASAP Validation Library Architecture

## Two execution contexts

1. **Development/source context:** `src/validation_library/` contains the new Python modules for maintainable authoring and isolated testing. `ValidationEngine` dispatches to provided GF methods with `getattr(gf, gf_function_name)`.
2. **ASAP host context:** The current host scripts must remain executable as **single scripts with one first callable entry point**. The older `host_compatible/host_compatible_design.md` documents that cross-script calls in this ASAP environment reach only the first function and cannot share a constructed Python instance. The modular package is **not** directly deployed into that environment until tested.

A small adapter isolates those contexts. The deployment builder assembles only legacy host-compatible scripts from the canonical source files. This branch does **not** generate, replace or deploy any production `ValidationEngine` GF script.

## Responsibilities

- `runtime/asap_adapter.py`: Resolve a known GF name on an injected `gf` namespace. `gf_v1` calls `(runtime_context=..., params=..., include_results=..., include_pass=...)`; `payload_v1` calls `(payload, runtime_context=...)`. No dynamic file imports.
- `core/registry.py`: Validate explicitly defined rules, function names, call style and portfolio membership.
- `core/context.py`: Resolve `runtime_context_key` and explicit runtime inputs.
- `core/engine.py`: Orchestrate rules and apply two-layer output filtering plus severity-based interruption.
- `core/result_contract.py`: Normalize bool, list and dict returns with an explicit pass/fail signal, fail closed for ambiguous output.
- `helpers/`: Single source for the existing standalone helper API used by deployed functions.
- `rules/`: Byte-identical *source mirrors* of currently implemented rules. Empty package folders indicate planned asset classes, not implemented checks.

## Existing host functions vs planned library

`ValidationEngine01.md` and `ValidationEngine02.md` are design prompts (not executable implementations). This migration introduces a separate, testable implementation for development. It does not claim feature parity with all options in the two documents, especially host printing, portfolio definitions and runtime object routing. Confirm these with approved ASAP UAT before integrating.

The sample registry is for illustration only. A deployed GF function name, exact return schema and asset-class applicability must be independently verified in host.

## Folder naming

Legacy scripts use `SetUp` and `Periodic`. The requested target folders use `setup` and `payment`. During migration, `Periodic` examples are parked under `payment` only for intended organization; do **not** interpret this as proof that every periodic check belongs only to payment processing. Review categorization with domain owners before production registry publication.
