# Git, Release and Deployment Process

## Branch policy (existing repo uses `master`)

- `master`: existing protected production/default line; leave unchanged until PR approved.
- `develop`: optional long-lived integration branch (not created in this migration; introduce only when team workflow requires it).
- `feature/*` and `refactor/*`: scoped changes via PR.
- `release/*`: stabilization, UAT and approval before merging to production.
- `hotfix/*`: emergency fix from the exact deployed production commit and synchronizing that fix back into development.

Do not create one persistent Git branch per Deal. Per-Deal variation belongs in approved versioned configurations after verifying actual ASAP host support for side-by-side versions.

## Release controls

1. Freeze approved code, registry and Deal configuration; run all CI checks.
2. Build `dist/asap/`, record SHA-256 hashes from `artifact_manifest.json`.
3. Execute real ASAP host UAT with authorized sanitized or controlled non-prod data.
4. Obtain code and business approvals, record diff to golden outputs.
5. Merge reviewed PR to `master`, create a semantic version Tag (e.g. `v1.0.0`) **only after approval**.
6. Deploy the exactly approved artifact through the organization's authorized process; track Deal/Portfolio consumers and runtime IDs.
7. Verify live version and keep last approved bundle/config ready for rollback.

Git Tag and `library_version` metadata do not automatically deploy or pin an ASAP GF. If the host shares one global function across Deals, shared code upgrades affect all consumers regardless of each Deal's sample manifest.

## Hotfix and rollback

Do not force-push to reverse a deploy. Create a `hotfix/*` branch from the deployed commit, test on impacted portfolios, approve the change, rebuild an immutable artifact, and follow release controls. Roll back using the approved code AND matching registry/config, not merely by changing the Git branch pointer.
