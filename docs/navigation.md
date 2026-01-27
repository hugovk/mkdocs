# Interlinking & Navigation

Navigation within your documentation is handled by using [document interlinking](#interlinking), and optional [site-wide navigation](#navigation).

## Interlinking

Use relative markdown links to allow users to navigate between documents.

For example, a website with `README.md` and `CONTRIBUTING.md` pages, might include the following&hellip;

```markdown
See our [contribution documentation](CONTRIBUTING.md) for more details on getting involved.
```

If your site includes pages within a directory structure, the page interlinking might also include [relative paths between directories](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#relative-links).

## Navigation

You can include site-wide navigation by using the `mkdocs.toml` configuration.

This is typically used by the HTML styling to include a navigation menu.

```toml
[mkdocs]
nav = [
    {title="Introduction", path="index.md"},
    {title="Writing Markdown", path="markdown.md"},
    {title="Site Navigation", path="navigation.md"},
    {title="HTML Styling", path="styling.md"}
]
```

This allows the theme to display navigation controls, as well as including `← previous` and `next →` links.

The navigation configuration can also include nested elements.

```toml
[mkdocs]
nav = [
    {title="Introduction", path="index.md"},
    {title="Tutorial", children=[
        {title="Creating a project", path="tutorial/new.md"},
        {title="Adding pages", path="tutorial/pages.md"},
        {title="Publishing your work", path="tutorial/publish.md"},
    ]},
    {title="Topics", children=[
        {title="Page layouts", path="topics/layouts.md"},
        {title="Typography", path="topics/typography.md"},
        {title="Color schemes", path="topics/schemes.md"},
    ]}
]
```

## URL Structure

Ensuring your website has a clean, meaningful URL structure is important for navigation.

* Markdown pages are lowercased.
* The file extension is not included in the URL.
* Use either `index.md` or `README.md` for root URLs.

**Examples**

A standard documentation site...

| **Markdown Page** | **HTML output**         | **URL**        |
|-------------------|-------------------------|----------------|
| `index.md`        | `index.html`            | `/`            |
| `markdown.md`     | `markdown/index.html`   | `/markdown/`   |
| `navigation.md`   | `navigation/index.html` | `/navigation/` |
| `styling.md`      | `styling/index.html`    | `/styling/`    |

<br/>

Uppercase filenames and GitHub style document paths...

| **Markdown Page** | **HTML output**          | **URL**        |
|-------------------|--------------------------|----------------|
| `README.md`       | `index.html`             | `/`            |
| `ABOUT.md`        | `about.html`             | `/about/`      |

<br/>

Documentation structure including subdirectories...

| **Markdown Page**        | **HTML output**                  | **URL**                 |
|--------------------------|----------------------------------|-------------------------|
| `index.md`               | `index.html`                     | `/`                     |
| `tutorial/quickstart.md` | `tutorial/quickstart/index.html` | `/tutorial/quickstart/` |
| `tutorial/next-steps.md` | `tutorial/next-steps/index.html` | `/tutorial/next-steps/` |

<br/>
