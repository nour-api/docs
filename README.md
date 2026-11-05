# Nour-API documentation

This checkout is the deployed Docusaurus output on `gh-pages`, served beneath `/docs/`. It contains no Docusaurus source project or build configuration. The sibling `nour-api.github.io` checkout contains another generated site with a different base path. Do not edit minified JavaScript or invent a missing Docusaurus build pipeline.

The maintained engineering guide is generated from **`guide/source.json` and `examples/application.php`**. This is the canonical source for the guide in both checkouts. Historical generated pages are retained and need a future rebuild from their original source.

```sh
python3 tools/render-guide.py --mirror ../nour-api.github.io
python3 tools/render-guide.py --mirror ../nour-api.github.io --check
php tools/test-examples.php
```

The last command uses `../framework/vendor/autoload.php` by default; an alternate autoloader may be passed as its first argument. It executes seven HTTP scenarios against the complete example. No deployment command is provided or required. Review the generated `guide/index.html` locally before publication.

## Development CI

The documentation workflow checks this canonical guide and the `nour-api.github.io` mirror from `dev` without modifying either file. It executes the seven documented HTTP scenarios against the checked-out framework `dev` branch on PHP 8.2 and 8.5, checks PHP syntax and audits the runtime dependencies. The tested framework commit is recorded in the run log.

The mirror repository runs the same canonical renderer and examples, using its own checked-out mirror files. Both workflows have read-only repository permissions and contain no deployment steps.

When changing the guide, render and commit both repositories, push both development branches, and rerun a drift check if it ran before the second push arrived. Framework-only changes do not trigger these repositories automatically; rerun their checks after coordinated kernel changes. Pushes to `dev`, pull requests and a declared manual dispatch trigger are supported.
