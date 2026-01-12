# HTML Styling

Styling is handled with HTML templating and regular web design.

## Templates

Anything in the `/templates/` directory is treated as a [Jinja template](https://jinja.palletsprojects.com/en/stable/templates/), and is used to render markdown pages. You can override templates locally and adapt them to make layout changes.

The base template for rendering markdown pages is **`templates/base.html`**. 

```html
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ config['site']['title'] }}</title>
        <link rel="icon" href="data:image/svg+xml,{% include 'favicon.svg' %}">
        <link rel="stylesheet" href="/css/highlightjs.min.css">
        <link rel="stylesheet" href="/css/highlightjs-copy.min.css">
        <link rel="stylesheet" href="/css/theme.css">
        <script src="/js/highlightjs.min.js"></script>
        <script src="/js/highlightjs-copy.min.js"></script>
        <script src="/js/theme.js"></script>
    </head>
    <body>
        <nav class="left">
            {{ nav }}
        </nav>
        <nav class="right">
            {{ toc }}
        </nav>
        <main>
            {{ content }}
            {% include "pagination.html" %}
        </main>
    </body>
</html>
```

The following templates are included in [the default theme](https://github.com/encode/mkdocs/blob/main/src/mkdocs/theme/)...

* `templates/base.html`- The base template used for rendering markdown pages.
* `templates/favicon.svg` - an SVG used for the favicon, that displays the `config['site']['favicon']` emoji.
* `templates/pagination.html` - Included by the base template. Renders next and previous page controls.

## Media

Any files that are not Markdown pages `*.md`, or templates `/templates/*`, are treated as media documents and are included in the website without modification.

This can include images, stylesheets, javascript, fonts, video and audio.

The default theme includes the following media documents...

* [`css/theme.css`](css/theme.css)
* [`css/highlightjs.min.css`](css/highlightjs.min.css)
* [`css/highlightjs-copy.min.css`](css/highlightjs-copy.min.css)
* [`js/theme.js`](js/theme.js)
* [`js/highlightjs.min.js`](js/highlightjs.min.js)
* [`js/highlightjs-copy.min.js`](js/highlightjs-copy.min.js)

You can override these locally to style the color scheme, the typography & layout, or to adapt the `highlight.js` code highlighting.
