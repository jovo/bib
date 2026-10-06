# bib

Central BibTeX library for Yumzu's repos. Paperpile writes `references.bib` here through its BibTeX sync. Do not edit it by hand. Paperpile overwrites the file on each sync.

## Use in a project repo

Add this repo as a submodule:

```bash
git submodule add https://github.com/jovo/bib.git bib
```

Point the build at `bib/references.bib`. Pull new references with:

```bash
git submodule update --remote bib
```

A submodule pins one commit, so a tagged paper keeps the references it was built with.
