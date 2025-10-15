# MkDocs

MkDocs is a smart, simple website design tool using [Markdown](writing.md), [templated HTML](styling.md#templates), and static [media files](styling.md#media).

## Installation

Install the mkdocs command line tool...

```shell
$ pip install mkdocs
```

## Getting started

1. Create a `README.md` file, and get authoring.
2. Run `mkdocs serve` to view your documentation in a browser.
3. Run `mkdocs build` to build a static website ready to host.

MkDocs supports [GitHub Flavored Markdown](writing.md) for page authoring.

## Adding pages

1. Create other markdown files, such as `CONTRIBUTING.md`.
2. Link between your documents, eg. `See the [contributing](CONTRIBUTING.md) page for more details`.
3. Create a `mkdocs.json` config file to add site navigation.

Sites can be single page, multipage, or deeply nested. Just use regular interlinking between your markdown documents, with `mkdocs.json` to define an overall [site layout](navigation.md).

## Custom styling

1. Create a `templates/base.html` file to customise the layout.
2. Create a `css/base.css` file to override the default styles.
3. Create a `js/base.css` file to override the default scripts.

Simple [styling adaptations](styling.md) include customising the colour scheme, the typography, or choosing the code highlighting style.
