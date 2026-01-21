# MkDocs

MkDocs is a smart, simple, website design tool.

## Installation

Install the `mkdocs` command line tool...

```shell
$ pip install git+https://github.com/encode/mkdocs.git
```

## Getting started

Create a `mkdocs.toml` config file.

```toml
[mkdocs]
nav = [
    {title="Homepage", path="README.md"},
]
```

Create a `docs/README.md` page. *MkDocs supports [GitHub Flavored Markdown](writing.md) for page authoring.*

```markdown
# MkDocs

Let's get writing.
```

Run `mkdocs serve` to view your documentation in a browser.

## Adding pages

1. Create additional markdown pages.
2. Use [markdown interlinking](navigation.md#interlinking) between pages.
3. Edit the `mkdocs.toml` config file to define [the site navigation](navigation.md#navigation).

## Custom styling

Styling adaptations can be kept simple, such as customising the colour scheme, or more comprehensive, such as creating an entirely new theme.

1. Modify [the HTML templating](styling.md#templates) to customise the layout.
2. Override or add [CSS and JavaScript](styling.md#statics) static assets.
