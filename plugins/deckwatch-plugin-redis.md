# deckwatch-plugin-redis

Adds a Redis sidecar to all application deployments. Injects REDIS_URL.

## Installation

Install via the deckwatch Marketplace page, or add to your plugin settings manually:

```json
{
  "name": "redis",
  "enabled": true,
  "source": {
    "type": "github",
    "repo": "alexconrey/deckwatch-plugin-redis",
    "ref": "v0.1.0",
    "path": "dist/plugin.wasm",
    "use_release": true
  }
}
```

## Usage

Associate the plugin with an application, then open the **Infrastructure** tab and click **+ Add Redis**.

## Source

[github.com/alexconrey/deckwatch-plugin-redis](https://github.com/alexconrey/deckwatch-plugin-redis)
