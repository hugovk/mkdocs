# MkDocs

MkDocs is a smart, simple, website design tool.

## Installation

Install the `mkdocs` command line tool...

```shell
$ pip install git+https://github.com/encode/mkdocs.git
```

This will install the *[version 2.0 pre-release](roadmap.md)*.

## Getting started

1. Create a `README.md` page.
2. Run `mkdocs serve` to view your documentation in a browser.
3. Run `mkdocs build` to build a static website ready to host.

*MkDocs supports [GitHub Flavored Markdown](writing.md) for page authoring.*

## Writing your docs

1. Create additional markdown pages.
2. Use [markdown interlinking](navigation.md#interlinking) between pages.
3. Create a `mkdocs.toml` file to define [the site navigation](navigation.md#navigation) and other configuration.
4. Move your markdown pages into a `docs` directory, and [configure the theme](styling.md#themes).

An example `mkdocs.toml`...

```toml
[mkdocs]
nav = [
    {path: "README.md", title: "Introduction"},
    {path: "CREDITS.md", title: "Credits"},
]
loaders = [
    {package: "mkdocs:theme"},
    {directory: "docs"},
]
```

*Use either [`README.md` or `index.md`](navigation.md#url-structure) for the homepage.*

## Custom styling

Styling adaptations can be kept simple, such as customising the colour scheme, or more comprehensive, such as creating an entirely new theme.

1. Modify [the HTML templating](styling.md#templates) to customise the layout.
2. Override or add [CSS and JavaScript](styling.md#statics) static assets.

## Legacy compatability

*Work is planned to handle compatability for both [mkdocs 1.x](https://www.mkdocs.org/) and [mkdocs 2.x](https://www.encode.io/mkdocs/) sites.*
