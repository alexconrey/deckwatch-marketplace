# deckwatch-plugin-otel

Adds an OpenTelemetry Collector sidecar. Injects OTEL_EXPORTER_OTLP_ENDPOINT.

## Installation

Install via the deckwatch Marketplace page, or add to your plugin settings manually:

```json
{
  "name": "otel",
  "enabled": true,
  "source": {
    "type": "github",
    "repo": "alexconrey/deckwatch-plugin-otel",
    "ref": "v0.1.0",
    "path": "dist/plugin.wasm",
    "use_release": true
  }
}
```

## Usage

Associate the plugin with an application, then open the **Infrastructure** tab and click **+ Add Otel**.

## Source

[github.com/alexconrey/deckwatch-plugin-otel](https://github.com/alexconrey/deckwatch-plugin-otel)
