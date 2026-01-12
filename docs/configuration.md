# Configuration

Site navigation and other configuration is defined in a `mkdocs.toml` file.

```toml
[mkdocs]
nav = [
    {title="Introduction", path="index.md"},
    {title="Writing Markdown", path="writing.md"},
    {title="Site Navigation", path="navigation.md"},
    {title="HTML Styling", path="styling.md"}
]
```

Navigation can include subsections...

```toml
[mkdocs]
nav = [
    {title="Introduction", path="README.md"},
    {title="Guides", children=[
        {title="Writing Markdown", path="writing.md"},
        {title="Site Navigation", path="navigation.md"},
        {title="HTML Styling", path="styling.md"}
    ]}
]
```

### Loaders

Loaders determine where documentation resources are collected from.

```toml
loaders = [
    {type="directory", dir="docs"},
    {type="package", pkg="mkdocs.theme"}
]
```

Customise this to load a different theme, from a ZIP archive...

```toml
loaders = [
    {type="directory", dir="docs"},
    {type="url", url="https://www.example.com/theme.zip"}
]
```

Or from a GitHub repo...

```toml
loaders = [
    {type="directory", dir="docs"},
    {type="github", url="mkdocs/default"}
]
```

<!--
### Markdown

The derault set of extensions are geared towards GitHub Flavored Markdown.

```toml
[markdown]
extensions = {...}
config = {...}
```

### Resources

Resources include markdown pages, static media, and HTML templates.

* `pages`      - `*.md`
* `statics`    - `*` 
* `templates`  - `templates/*`

### Commands

The command line tool allows you to work with mkdocs locally,
or to build and host your sites on a provider of your choosing.

* `mkdocs serve`
* `mkdocs build`
-->