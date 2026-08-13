# deckwatch-plugin-memcached

Adds a Memcached sidecar to all application deployments. Injects MEMCACHED_URL.

## Installation

Install via the deckwatch Marketplace page, or add to your plugin settings manually:

```json
{
  "name": "memcached",
  "enabled": true,
  "source": {
    "type": "github",
    "repo": "alexconrey/deckwatch-plugin-memcached",
    "ref": "v0.1.0",
    "path": "dist/plugin.wasm",
    "use_release": true
  }
}
```

## Usage

Associate the plugin with an application, then open the **Infrastructure** tab and click **+ Add Memcached**.

## Source

[github.com/alexconrey/deckwatch-plugin-memcached](https://github.com/alexconrey/deckwatch-plugin-memcached)
