# deckwatch-plugin-postgresql

Adds a PostgreSQL sidecar with PVC. Injects PG_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, PGDATA.

## Installation

Install via the deckwatch Marketplace page, or add to your plugin settings manually:

```json
{
  "name": "postgresql",
  "enabled": true,
  "source": {
    "type": "github",
    "repo": "alexconrey/deckwatch-plugin-postgresql",
    "ref": "v0.1.0",
    "path": "dist/plugin.wasm",
    "use_release": true
  }
}
```

## Usage

Associate the plugin with an application, then open the **Infrastructure** tab and click **+ Add Postgresql**.

## Source

[github.com/alexconrey/deckwatch-plugin-postgresql](https://github.com/alexconrey/deckwatch-plugin-postgresql)
