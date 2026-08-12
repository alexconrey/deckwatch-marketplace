# deckwatch marketplace

The official plugin catalog for [deckwatch](https://github.com/alexconrey/deckwatch),
a Kubernetes operator that provisions cloud resources from workload annotations.

The catalog is served as a static site at **https://market.deckwatch.io** via
GitHub Pages. deckwatch fetches the machine-readable catalog client-side from:

```
https://market.deckwatch.io/catalog.json
```

---

## Browsing plugins in deckwatch

Go to **Settings → Marketplace** in the deckwatch UI. The operator fetches the
catalog on demand and displays available plugins with trust level indicators.

---

## Installing a plugin that isn't in the marketplace

You can install any WASM plugin directly without it being listed in this catalog:

1. Go to **Settings → Plugins → Add**
2. Choose source type **GitHub** or **URL**
3. Enter the repo/ref/path (GitHub) or a direct HTTPS URL to the `.wasm` file
4. Confirm the host allowlist when prompted

---

## Self-hosting the catalog for air-gapped environments

For clusters without outbound internet access:

1. Mirror `catalog.json` to an internal HTTPS server
2. For each plugin entry, host the `.wasm` file internally and change
   `source.type` to `"url"` with the internal URL
3. Configure deckwatch to use your internal catalog URL instead of
   `https://market.deckwatch.io/catalog.json` (see deckwatch operator docs)

Note: `source.type: "github"` entries still resolve WASM binaries from GitHub
Releases — change them to `"url"` entries pointing at your internal mirror
before using in an air-gapped environment.

---

## Submitting a plugin

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full submission process, schema
reference, and trust level requirements.

---

## Catalog schema version

This catalog uses schema `version: 1`. Breaking changes to the schema will
increment this version number and will be accompanied by a migration guide.
