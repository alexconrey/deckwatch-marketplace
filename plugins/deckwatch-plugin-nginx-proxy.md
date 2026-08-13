# deckwatch-plugin-nginx-proxy

Adds an Nginx reverse proxy sidecar. Configurable port (80, 443, 8080).

## Installation

Install via the deckwatch Marketplace page, or add to your plugin settings manually:

```json
{
  "name": "nginx-proxy",
  "enabled": true,
  "source": {
    "type": "github",
    "repo": "alexconrey/deckwatch-plugin-nginx-proxy",
    "ref": "v0.1.0",
    "path": "dist/plugin.wasm",
    "use_release": true
  }
}
```

## Usage

Associate the plugin with an application, then open the **Infrastructure** tab and click **+ Add Nginx Proxy**.

## Source

[github.com/alexconrey/deckwatch-plugin-nginx-proxy](https://github.com/alexconrey/deckwatch-plugin-nginx-proxy)
