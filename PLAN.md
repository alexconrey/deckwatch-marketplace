# deckwatch-marketplace — Implementation Plan

This repository is the centralized catalog for the deckwatch plugin marketplace,
served via GitHub Pages. It is a purely static site — no server required.

When complete, `http://market.deckwatch.io/catalog.json` will return the
machine-readable plugin catalog that the deckwatch frontend fetches client-side.

---

## Repository structure to create

```
deckwatch-marketplace/
  catalog.json                        # Machine-readable plugin catalog (GitHub Pages)
  index.html                          # Human-readable landing page (GitHub Pages)
  plugins/
    deckwatch-plugin-aws.md           # Human-readable AWS plugin page
  .github/
    scripts/
      validate_catalog.py             # Validation script run in CI
    workflows/
      validate.yml                    # PR check: validate catalog.json
      publish.yml                     # On merge to main: publish to GitHub Pages
  CONTRIBUTING.md                     # How to submit a plugin
  README.md                           # Overview and usage instructions
```

---

## 1. catalog.json

The root `catalog.json` is the file deckwatch fetches. It must be valid JSON and
conform to the schema below at all times.

```json
{
  "version": 1,
  "updated_at": "2026-08-12T00:00:00Z",
  "plugins": [
    {
      "name": "AWS",
      "slug": "deckwatch-plugin-aws",
      "description": "Provisions IAM roles, RDS databases, and S3 buckets for Kubernetes workloads with a unified per-workload IAM role.",
      "author": "alexconrey",
      "homepage": "https://github.com/alexconrey/deckwatch-plugin-aws",
      "trust_level": "verified",
      "tags": ["aws", "rds", "s3", "iam", "irsa"],
      "latest_version": "0.3.0",
      "source": {
        "type": "github",
        "repo": "alexconrey/deckwatch-plugin-aws",
        "ref": "v0.3.0",
        "path": "plugin.wasm",
        "use_release": true
      },
      "allowed_hosts_hint": ["*.amazonaws.com", "iam.us-gov.amazonaws.com"]
    }
  ]
}
```

### Field definitions

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | Display name shown in deckwatch UI |
| `slug` | string | yes | Unique identifier, kebab-case, matches repo name convention |
| `description` | string | yes | One or two sentences |
| `author` | string | yes | GitHub username or org |
| `homepage` | string | yes | Link to plugin repo or docs |
| `trust_level` | `"verified"` or `"community"` | yes | `verified` requires maintainer review |
| `tags` | string[] | yes | Lowercase, used for filtering |
| `latest_version` | string | yes | Semver without leading `v` |
| `source` | object | yes | Same schema as deckwatch `PluginConfig.source` |
| `source.type` | `"github"` or `"url"` | yes | |
| `source.repo` | string | if github | `"owner/repo"` |
| `source.ref` | string | if github | Must be a tag (validated in CI) |
| `source.path` | string | if github | Path to `.wasm` file in release assets |
| `source.use_release` | bool | if github | Whether to fetch from GitHub Releases |
| `allowed_hosts_hint` | string[] | no | Suggested `allowed_hosts` for deckwatch to pre-fill on install |

---

## 2. .github/scripts/validate_catalog.py

Write a Python 3 script (no external dependencies beyond stdlib + `json`) that:

1. Reads `catalog.json` from the repo root
2. Validates the top-level structure: `version` (int), `updated_at` (ISO 8601 string), `plugins` (array)
3. For each plugin entry, validates:
   - All required fields are present and non-empty strings
   - `trust_level` is exactly `"verified"` or `"community"`
   - `slug` matches pattern `^[a-z0-9-]+$`
   - `source.type` is `"github"` or `"url"`
   - If `source.type == "github"`: `ref` exists and matches `^v[0-9]+\.[0-9]+` (must be a tag, not a branch)
   - `latest_version` matches `^[0-9]+\.[0-9]+\.[0-9]+` (semver without `v` prefix)
   - No duplicate `slug` values
4. Exits with code 0 on success, prints errors and exits with code 1 on failure
5. Prints a summary: `Validated N plugins — all OK` or lists all validation errors

---

## 3. .github/workflows/validate.yml

Trigger: `pull_request` targeting `main`, on changes to `catalog.json` or
`.github/scripts/validate_catalog.py`.

Steps:
1. `actions/checkout@v4`
2. `actions/setup-python@v5` with Python 3.12
3. Run `python .github/scripts/validate_catalog.py`

```yaml
name: Validate catalog
on:
  pull_request:
    branches: [main]
    paths:
      - catalog.json
      - .github/scripts/validate_catalog.py

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Validate catalog.json
        run: python .github/scripts/validate_catalog.py
```

---

## 4. .github/workflows/publish.yml

Trigger: `push` to `main`.

Publishes the repo contents to GitHub Pages using `actions/deploy-pages`. The
entire repo root is the Pages source — `catalog.json` and `index.html` are served
at the repo's Pages URL.

```yaml
name: Publish to GitHub Pages
on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - id: deployment
        uses: actions/deploy-pages@v4
```

After this workflow runs, `catalog.json` is available at the GitHub Pages URL for
the repo. The custom domain `deckwatch.io` must be configured in repo Settings →
Pages → Custom domain.

---

## 5. index.html

A simple human-readable landing page served at the root. Should:
- Display the marketplace name and description
- Link to `catalog.json` for direct access
- List the plugins in `catalog.json` (can be static HTML, no JavaScript required)
- Link to `CONTRIBUTING.md`

Keep it minimal and dependency-free. Inline CSS only, no external frameworks.

---

## 6. plugins/deckwatch-plugin-aws.md

A human-readable page for the AWS plugin. Content to include:
- Plugin name, version, author
- Description of what it provisions (IAM roles, RDS, S3)
- Prerequisites (deckwatch running, AWS credentials via IRSA or static keys)
- Configuration fields: `AWS_REGION`, `IAM_ENDPOINT`, `IAM_SIGNING_REGION`, `ROLE_PATH`, `BUCKET_PREFIX`
- Annotation reference: `aws.deckwatch.io/enabled`, `rds.deckwatch.io/*`, `s3.deckwatch.io/*`
- How to install via deckwatch UI (Settings → Plugins → Add) or via the Marketplace page
- Link to the plugin's GitHub repo: https://github.com/alexconrey/deckwatch-plugin-aws

---

## 7. CONTRIBUTING.md

Instructions for submitting a plugin. Cover:

### Submission process
1. Fork this repository
2. Add an entry to `catalog.json` following the schema above
3. Add a human-readable page at `plugins/{slug}.md`
4. Open a pull request
5. CI will validate `catalog.json` automatically
6. For `trust_level: "verified"`: maintainer review and approval is required
7. For `trust_level: "community"`: CI passing is sufficient to merge

### Trust levels
- **verified** — The deckwatch project team has reviewed the plugin source code,
  confirmed it does not exfiltrate data or execute unexpected network calls, and
  approved the `allowed_hosts` list. Requires maintainer sign-off on the PR.
- **community** — The plugin author has submitted the entry but it has not been
  reviewed by the deckwatch project. Deckwatch displays a warning to operators
  before installation.

### Requirements for all submissions
- `source.ref` must be a release tag (e.g. `v1.2.3`), not a branch name
- The referenced WASM binary must be publicly downloadable without authentication
- `description` must be one to two sentences, plain text
- `tags` should use existing tags where possible to aid discoverability

---

## 8. README.md

Overview document. Cover:
- What this repository is (the official deckwatch plugin marketplace catalog)
- How deckwatch uses it (fetched client-side from `http://market.deckwatch.io/catalog.json`)
- How to browse plugins in deckwatch (Settings → Marketplace page)
- How to install a plugin that isn't in the marketplace (custom URL/GitHub source in settings)
- How to self-host the catalog for air-gapped environments
- Link to CONTRIBUTING.md for plugin authors

---

## 9. GitHub Pages setup (manual step after repo is created)

After CI is in place:
1. Go to repo Settings → Pages
2. Source: GitHub Actions
3. Custom domain: `deckwatch.io` (once DNS is configured)
4. Enforce HTTPS: yes

This is a one-time manual configuration — the `publish.yml` workflow handles
all subsequent deployments automatically.

---

## Implementation notes for agent teams

- All files should be committed on a branch and merged via PR (never push directly to main)
- The `validate.yml` check must pass on the initial PR that adds `catalog.json`
- `updated_at` in `catalog.json` should be set to the current date in ISO 8601 format
- The `index.html` should be self-contained (no CDN dependencies) so it works in air-gapped mirror deployments
- Do not include any secrets or tokens in any file
