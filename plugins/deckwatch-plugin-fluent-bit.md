# deckwatch-plugin-fluent-bit

Adds a Fluent Bit log-shipping sidecar. Configurable output endpoint.

## Installation

Install via the deckwatch Marketplace page, or add to your plugin settings manually:

```json
{
  "name": "fluent-bit",
  "enabled": true,
  "source": {
    "type": "github",
    "repo": "alexconrey/deckwatch-plugin-fluent-bit",
    "ref": "v0.1.0",
    "path": "dist/plugin.wasm",
    "use_release": true
  }
}
```

## Usage

Associate the plugin with an application, then open the **Infrastructure** tab and click **+ Add Fluent Bit**.

## Source

[github.com/alexconrey/deckwatch-plugin-fluent-bit](https://github.com/alexconrey/deckwatch-plugin-fluent-bit)
