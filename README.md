# Nour-API documentation

This checkout is the deployed Docusaurus output on `gh-pages`, served beneath `/docs/`. It contains no Docusaurus source project or build configuration. The sibling `nour-api.github.io` checkout contains another generated site with a different base path. Do not edit minified JavaScript or invent a missing Docusaurus build pipeline.

The maintained engineering guide is generated from **`guide/source.json` and `examples/application.php`**. This is the canonical source for the guide in both checkouts. Historical generated pages are retained and need a future rebuild from their original source.

```sh
python3 tools/render-guide.py --mirror ../nour-api.github.io
python3 tools/render-guide.py --mirror ../nour-api.github.io --check
php tools/test-examples.php
```

The last command uses `../framework/vendor/autoload.php` by default; an alternate autoloader may be passed as its first argument. It executes seven HTTP scenarios against the complete example. No deployment command is provided or required. Review the generated `guide/index.html` locally before publication.
