# MkDocs

MkDocs is a smart, simple, website design tool.

## Installation

Install the `mkdocs` command line tool...

```shell
$ pip install git+https://github.com/encode/mkdocs.git
```

## Getting started

1. Create a `README.md` page.
2. Run `mkdocs serve` to view your documentation in a browser.
3. Run `mkdocs build` to build a static website ready to host.

MkDocs supports [GitHub Flavored Markdown](writing.md) for page authoring.

## Adding pages

1. Create additional markdown pages.
2. Use [markdown interlinking](navigation.md#interlinking) between pages.
3. Create a `mkdocs.toml` config file to define [the site navigation](navigation.md#navigation).

## Custom styling

1. Create a `templates/base.html` file to customise the layout.
2. Create a `css/base.css` file to override the default styles.
3. Create a `js/base.css` file to override the default scripts.

Simple [styling adaptations](styling.md) include customising the colour scheme, the typography, or choosing the code highlighting style.
