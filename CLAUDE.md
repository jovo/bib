# Shared bibliography

This repo holds one bibliography that serves all of the author's repos. Follow these rules when adding, fixing, or citing references from it.

- One bibliography serves all repos. Zotero holds the library. Better BibTeX auto-exports it as BibLaTeX to `references.bib` in the public repo `github.com/jovo/bib`, and a background job commits and pushes each change. Repos never keep their own `.bib`.
- Add, fix, or deduplicate references in Zotero, never by editing `references.bib`. Agents add papers with `~/github/bib/bin/addref <DOI or URL>`, which imports into the running Zotero. Zotero must be open.
- Repos read the bib from `https://raw.githubusercontent.com/jovo/bib/main/references.bib`. A repo with a build fetches it at build time (see `computational-connectomics/build/fetch-bib.sh`: cached offline, rewritten only on change, untracked in git). A standalone Markdown file sets it in YAML front matter as `bibliography: <that URL>`, which pandoc 3.9 reads directly. GitHub caches the raw file for about 5 minutes, so a new entry takes that long to reach builds.
- Citation keys come from Better BibTeX, formula `auth + shortyear`. Never hand-construct a key. Look it up in `references.bib`.
- Key shape is `SurnameYY` (e.g., `Friston10`). Hyphens and the stored case of particles are kept: `Aston-Jones00`, `vanRooij19`. On collision the first entry stays bare. Keys imported from Paperpile use `b`, `c`, ... for later entries (`DeSilva22`, `DeSilva22b`), and new keys use `a`, `b`, .... Entries missing author or year get `OtherOther...` keys. Fix the metadata in Zotero rather than citing those.
- `references.bib` is BibLaTeX.
