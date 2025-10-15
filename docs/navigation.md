# Site Navigation

When building sites with multiple pages, use `index.md` or `README.md` for root URLs.

| **File**            | **URL** |
|-----------------|-----|
| `index.md`      | `/`
| `markdown.md`   | `/markdown/`
| `navigation.md` | `/navigation/`
| `styling.md`    | `/styling/`

Pages should use the `.md` file extension in order to be rendered as markdown. Other documents are served unmodified as [media files](styling.md#media).

## Interlinking

Use relative interlinking to help users navigate between documents.

Link to another markdown file in the same directory&hellip;

```markdown
See our [contribution documentation](CONTRIBUTING.md) for more details on getting involved.
```

Link to a document in a subdirectory&hellip;

```markdown
The [tutorial](tutorial/getting-started.md) will help get you started.
```

Link to a document in a parent directory&hellip;

```markdown
Back to the [homepage](../index.md).
```

## Configuration

You can include site-wide navigation by using the `mkdocs.toml` configuration.

```
[mkdocs]
version = 2

[site]
title = "MkDocs"
favicon = "📘"
nav = [
    {title="Introduction", path="index.md"},
    {title="Writing Markdown", path="markdown.md"},
    {title="Site Navigation", path="navigation.md"},
    {title="HTML Styling", path="styling.md"}
]
```

This allows the theme to display navigation controls, as well as including `← previous` and `next →` links.