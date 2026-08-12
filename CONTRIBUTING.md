# Contributing a plugin to the deckwatch marketplace

Thank you for contributing! This document describes how to submit a plugin to the
deckwatch marketplace catalog.

---

## Submission process

1. **Fork** this repository
2. **Add a catalog entry** in `catalog.json` following the [schema below](#schema)
3. **Add a plugin page** at `plugins/{slug}.md` (use
   [plugins/deckwatch-plugin-aws.md](plugins/deckwatch-plugin-aws.md) as a template)
4. **Open a pull request** — CI will validate `catalog.json` automatically
5. For `trust_level: "verified"`: maintainer review and explicit approval are required
6. For `trust_level: "community"`: CI passing is sufficient to merge

---

## Trust levels

### verified

The deckwatch project team has:
- Reviewed the plugin source code
- Confirmed it does not exfiltrate data or execute unexpected network calls
- Approved the `allowed_hosts` list

Requires maintainer sign-off on the PR. Appropriate for plugins published and
maintained by known contributors.

### community

The plugin author has submitted the entry but it has not been reviewed by the
deckwatch project team. deckwatch displays a warning to cluster operators before
installation. Appropriate for plugins in early development or from new contributors.

---

## Requirements for all submissions

| Requirement | Details |
|---|---|
| `source.ref` must be a release tag | e.g. `v1.2.3` — branch names are rejected by CI |
| `source.ref` must equal `v` + `latest_version` | e.g. ref `v1.2.3` → latest_version `1.2.3` |
| WASM binary must be publicly downloadable | Without authentication, from a GitHub Release |
| `description` | One to two sentences, plain text, no markdown |
| `slug` | Lowercase kebab-case matching `^[a-z0-9-]+$`, globally unique |
| `tags` | Prefer existing tags where possible to aid discoverability |
| Plugin page | `plugins/{slug}.md` must be present in the same PR |

---

## Schema reference

```json
{
  "name": "My Plugin",
  "slug": "deckwatch-plugin-my-plugin",
  "description": "One or two sentences describing what the plugin provisions.",
  "author": "github-username",
  "homepage": "https://github.com/github-username/deckwatch-plugin-my-plugin",
  "trust_level": "community",
  "tags": ["aws", "storage"],
  "latest_version": "1.0.0",
  "source": {
    "type": "github",
    "repo": "github-username/deckwatch-plugin-my-plugin",
    "ref": "v1.0.0",
    "path": "plugin.wasm",
    "use_release": true
  },
  "allowed_hosts_hint": ["*.example.com"]
}
```

`allowed_hosts_hint` is optional but strongly recommended — it pre-fills the
host allowlist that deckwatch shows the operator at install time.

---

## Local validation

Before opening a PR, run the validator locally:

```bash
python .github/scripts/validate_catalog.py
```

This checks the same rules as CI.

---

## Questions?

Open an issue in [alexconrey/deckwatch-marketplace](https://github.com/alexconrey/deckwatch-marketplace/issues).
