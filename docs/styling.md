# Themes & Styling

Styling is handled with HTML templating and regular web design.

The build is made up of various web resources...

* [Templates](#templates) - *The HTML templates used to render documentation pages.*
* [Pages](#pages) - *The markdown files comprising the documentation.*
* [Statics](#statics) - *Media assests including images, CSS, and JavaScript.*

Resources are loaded either from a *theme* or from the *project documentation*. The theme system allows minor local styling overrides, or complete site customisation.

* [Themes](#themes) - *Theme and documentation configuration is handled in the `mkdocs.toml` file.*

## Templates

Anything in the `/templates/` directory is treated as a [Jinja template](https://jinja.palletsprojects.com/en/stable/templates/), and is used to render markdown pages. You can override templates locally and adapt them to make layout changes.

The base template for rendering markdown pages is **`templates/base.html`**. 

```html
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ config.mkdocs.title or page.title }}</title>
        <link rel="icon" href="data:image/svg+xml,&lt;svg xmlns=&quot;http://www.w3.org/2000/svg&quot; viewBox=&quot;0 0 100 100&quot;&gt;&lt;text y=&quot;.9em&quot; font-size=&quot;90&quot;&gt;{{ config.mkdocs.favicon or '📘' }}&lt;/text&gt;&lt;/svg&gt;">
        <link rel="stylesheet" href="{{ '/css/highlightjs.min.css' | url }}">
        <link rel="stylesheet" href="{{ '/css/highlightjs-copy.min.css' | url }}">
        <link rel="stylesheet" href="{{ '/css/theme.css' | url }}">
        <script src="{{ '/js/highlightjs.min.js' | url }}"></script>
        <script src="{{ '/js/highlightjs-copy.min.js' | url }}"></script>
        <script src="{{ '/js/theme.js' | url }}"></script>
    </head>
    <body>
        <nav class="left">
            {{ nav.html }}
        </nav>
        <nav class="right">
            {{ page.toc }}
        </nav>
        <main>
            {{ page.html }}
            {% if nav.previous or nav.next %}
            <div class="pagination">
                {% if nav.previous %}
                <a class="previous" href="{{ nav.previous.url }}">← {{ nav.previous.title }}</a>
                {% endif %}
                {% if nav.next %}
                <a class="next" href="{{ nav.next.url }}">{{ nav.next.title }} →</a>
                {% endif %}
            </div>
            {% endif %}
        </main>
    </body>
</html>
```

The following template is included in [the default theme](https://github.com/encode/mkdocs/blob/main/src/mkdocs/theme/)...

* `templates/base.html`- The base template used for rendering markdown pages.

The following context is passed to the template rendering...


*Variable*           | *Description*
---------------------|--------------------------------------
`page`               | The markdown page.
`page.html`          | The page contents, rendered as HTML.
`page.text`          | The text of the page, as markdown.
`page.path`          | The path of the source file.
`page.url`           | The URL from which the page is served.
`page.toc`           | The table of contents for the page, as HTML.
`page.title`         | The first heading in the table of contents.
`nav`                | The site navigation.
`nav.html`           | The site navigation, rendered into HTML.
`nav.previous`       | The previous page, as configured in the nav.
`nav.previous.title` | The title of the previous page.
`nav.previous.url`   | The url of the previous page.
`nav.next`           | The next page, as configured in the nav.
`nav.next.title`     | The title of the next page.
`nav.next.url`       | The url of the next page.
`config`             | The `mkdocs.toml` configuration.

## Pages

Any files ending with the `*.md` extension are treated as markdown pages, and rendered into HTML, then included in the base template.

The following are treated as index pages...

* `README.md` - Served as `/`.
* `index.md` - Served as `/`.

All other pages are lowercased, and served from a URL without the markdown extension...

* `CONTRIBUTING.md` - Served as `/contributing/`.

## Statics

Any files that are not Markdown pages `*.md`, or templates `/templates/*`, are treated as static media and are included in the website without modification.

This can include images, stylesheets, javascript, fonts, video and audio.

The default theme includes the following static media...

* [`css/theme.css`](css/theme.css)
* [`css/highlightjs.min.css`](css/highlightjs.min.css)
* [`css/highlightjs-copy.min.css`](css/highlightjs-copy.min.css)
* [`js/theme.js`](js/theme.js)
* [`js/highlightjs.min.js`](js/highlightjs.min.js)
* [`js/highlightjs-copy.min.js`](js/highlightjs-copy.min.js)

## Themes

Themes can be packaged and distributed as part of a zip archive. The archive can the either be loaded remotely from a URL, or downloaded and included locally.

Controlling how resources are loaded for the theme and documentation is handled with the `mkdocs.toml` config file.

**Example configurations**

*The default theme supplied by the `mkdocs` package, and the documentation served directly from the project directory. This is the default configuration...*

```toml
[mkdocs]
resources = [
    {package="mkdocs:theme"},
    {directory="."},
]
```

*The default theme as a `.zip` URL, and a local `docs` directory...*

```toml
[mkdocs]
resources = [
    {url="https://github.com/lovelydinosaur/test/archive/refs/heads/main.zip"},
    {directory="docs"},
]
```

*A theme downloaded locally, and a `docs` directory...*

```toml
[mkdocs]
resources = [
    {directory="theme"},
    {directory="docs"},
]
```

*Both the theme and the documentation included in a single directory...*

```toml
[mkdocs]
resources = [
    {directory="docs"},
]
```
