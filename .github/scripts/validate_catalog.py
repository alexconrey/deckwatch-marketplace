#!/usr/bin/env python3
"""Validates catalog.json against the deckwatch marketplace schema."""

import json
import os
import re
import sys

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
CATALOG_PATH = os.path.join(REPO_ROOT, "catalog.json")
PLUGINS_DIR = os.path.join(REPO_ROOT, "plugins")

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
# Strict semver tag: v1.2.3 (no pre-release suffixes for marketplace entries)
REF_RE = re.compile(r"^v[0-9]+\.[0-9]+\.[0-9]+$")
# Semver without leading v: 1.2.3
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")

REQUIRED_PLUGIN_FIELDS = [
    "name", "slug", "description", "author", "homepage",
    "trust_level", "tags", "latest_version", "source",
]

VALID_TRUST_LEVELS = {"verified", "community"}
VALID_SOURCE_TYPES = {"github", "url"}


def validate(catalog_path: str) -> list[str]:
    errors: list[str] = []

    try:
        with open(catalog_path, encoding="utf-8") as f:
            catalog = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Failed to parse catalog.json: {exc}"]

    # Top-level structure
    if not isinstance(catalog.get("version"), int):
        errors.append("top-level 'version' must be an integer")
    if not isinstance(catalog.get("updated_at"), str) or not catalog["updated_at"]:
        errors.append("top-level 'updated_at' must be a non-empty ISO 8601 string")
    if not isinstance(catalog.get("plugins"), list):
        errors.append("top-level 'plugins' must be an array")
        return errors  # can't continue without the plugins list

    seen_slugs: set[str] = set()

    for i, plugin in enumerate(catalog["plugins"]):
        prefix = f"plugins[{i}]"

        # Required fields present and non-empty
        for field in REQUIRED_PLUGIN_FIELDS:
            value = plugin.get(field)
            if value is None:
                errors.append(f"{prefix}: missing required field '{field}'")
            elif field not in ("tags", "source") and not isinstance(value, str):
                errors.append(f"{prefix}: '{field}' must be a string")
            elif isinstance(value, str) and not value.strip():
                errors.append(f"{prefix}: '{field}' must not be empty")

        slug = plugin.get("slug", "")

        # Slug format
        if slug and not SLUG_RE.match(slug):
            errors.append(f"{prefix}: 'slug' must match ^[a-z0-9-]+$ (got '{slug}')")

        # No duplicate slugs
        if slug in seen_slugs:
            errors.append(f"{prefix}: duplicate slug '{slug}'")
        elif slug:
            seen_slugs.add(slug)

        # trust_level
        trust = plugin.get("trust_level", "")
        if trust and trust not in VALID_TRUST_LEVELS:
            errors.append(
                f"{prefix}: 'trust_level' must be 'verified' or 'community' (got '{trust}')"
            )

        # tags must be an array of strings
        tags = plugin.get("tags")
        if tags is not None:
            if not isinstance(tags, list):
                errors.append(f"{prefix}: 'tags' must be an array")
            elif not all(isinstance(t, str) for t in tags):
                errors.append(f"{prefix}: all 'tags' entries must be strings")

        # latest_version format
        latest = plugin.get("latest_version", "")
        if latest and not VERSION_RE.match(latest):
            errors.append(
                f"{prefix}: 'latest_version' must be semver without 'v' prefix (got '{latest}')"
            )

        # source validation
        source = plugin.get("source")
        if isinstance(source, dict):
            src_type = source.get("type", "")
            if src_type not in VALID_SOURCE_TYPES:
                errors.append(
                    f"{prefix}.source: 'type' must be 'github' or 'url' (got '{src_type}')"
                )

            if src_type == "github":
                ref = source.get("ref", "")
                if not ref:
                    errors.append(f"{prefix}.source: 'ref' is required for type 'github'")
                elif not REF_RE.match(ref):
                    errors.append(
                        f"{prefix}.source: 'ref' must be a stable semver tag like v1.2.3 "
                        f"(got '{ref}')"
                    )
                elif latest and ref != f"v{latest}":
                    errors.append(
                        f"{prefix}: 'source.ref' ({ref}) must equal 'v' + 'latest_version' "
                        f"(v{latest})"
                    )

                if not source.get("repo"):
                    errors.append(f"{prefix}.source: 'repo' is required for type 'github'")

        elif source is not None:
            errors.append(f"{prefix}: 'source' must be an object")

        # Plugin page must exist
        if slug:
            page_path = os.path.join(PLUGINS_DIR, f"{slug}.md")
            if not os.path.isfile(page_path):
                errors.append(
                    f"{prefix}: missing plugin page at plugins/{slug}.md"
                )

    return errors


def main() -> int:
    errors = validate(CATALOG_PATH)
    plugin_count = 0
    try:
        with open(CATALOG_PATH, encoding="utf-8") as f:
            data = json.load(f)
        plugin_count = len(data.get("plugins", []))
    except Exception:
        pass

    if errors:
        print(f"catalog.json validation FAILED ({len(errors)} error(s)):\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"Validated {plugin_count} plugin(s) — all OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
