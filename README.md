# bib

Central BibLaTeX library for jovo's repos. Paperpile holds the library, and its automatic BibTeX export commits it to `references.bib` here. Do not edit `references.bib` by hand. The next export overwrites it.

## Use in a project repo

Read the file from GitHub instead of keeping a copy:

```
https://raw.githubusercontent.com/jovo/bib/main/references.bib
```

A repo with a build fetches it at build time with `bin/fetch-bib`, copied to `build/fetch-bib.sh` (see `computational-connectomics`). A standalone Markdown file names it in YAML front matter:

```yaml
---
bibliography: https://raw.githubusercontent.com/jovo/bib/main/references.bib
---
```

GitHub caches the raw file for about 5 minutes, so a new entry takes that long to reach builds after Paperpile exports it. Cite with the key exactly as it appears in `references.bib`.

## Add a reference

Add it in Paperpile: the web app, the browser extension, or an agent through the Paperpile MCP server. For Claude Code:

```bash
claude plugin marketplace add Paperpile/agent-plugins
```

```bash
claude plugin install paperpile@paperpile
```

Then sign in with `/mcp`. Paperpile assigns the citation key.

Run the tests with `python3 -m unittest discover tests`.
