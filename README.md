# bib

Central BibLaTeX library for jovo's repos. Zotero holds the library. Better BibTeX auto-exports it to `references.bib` here, and a background job commits and pushes each change. Do not edit `references.bib` by hand. The next export overwrites it.

## Use in a project repo

Read the file from GitHub instead of keeping a copy:

```
https://raw.githubusercontent.com/jovo/bib/main/references.bib
```

A repo with a build fetches it at build time (see `build/fetch-bib.sh` in `computational-connectomics`). A standalone Markdown file names it in YAML front matter:

```yaml
---
bibliography: https://raw.githubusercontent.com/jovo/bib/main/references.bib
---
```

GitHub caches the raw file for about 5 minutes, so a new entry takes that long to reach builds. Cite with the key exactly as it appears in `references.bib`.

## Add a reference

With Zotero open:

```bash
bin/addref 10.1016/j.nlm.2004.06.005
```

It takes a DOI, a paper URL, or `PMID:n`, imports the paper into Zotero, and prints its citation key. A DOI already in the library is not imported twice.

## Tools

- `bin/install` sets up the launchd agent that runs `bin/autocommit` when `references.bib` changes. Run it once per machine. The log is at `~/Library/Logs/bib-autocommit.log`.
- `bin/autocommit` waits for the export to settle, runs `bin/protect-titles`, then commits and pushes.
- `bin/protect-titles` wraps titles in double braces so CSL styles keep their casing.

Run the tests with `python3 -m unittest discover tests`.
