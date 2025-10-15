# Styling

Styling is handled with HTML templating and regular web design.

## Templates

Markdown documents are rendered using Jinja templating.

The following templates are included in the default theme...

* `templates/base.html`

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

The base template used for rendering markdown pages. You can override this template locally and adapt it to make layout changes.

* `templates/favicon.svg`

```html
{% set escaped %}<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">{{ config['site']['favicon'] }}</text></svg>{% endset %}{{ escaped | e }}
```

Included by the base template. This is an SVG used for the favicon, that is included as an inline `data:` URL.

Enables the `config['site']['favicon']` field to config a unicode emoji to use as the site favicon.

* `templates/pagination.html`

```html
{% if page.previous or page.next %}
<div class="pagination">
    {% if page.previous %}
    <a class="previous" href="{{ page.previous['url']}}">← {{ page.previous['title']}}</a>
    {% endif %}
    {% if page.next %}
    <a class="next" href="{{ page.next['url']}}">{{ page.next['title']}} →</a>
    {% endif %}
</div>
{% endif %}
```

Included by the base template. Renders next and previous page controls.

## Media

The default theme includes the following assets:

* [`css/theme.css`](css/theme.css) &mdash; Copy and overide this file in order to change the color palette, the typography, or to other style changes.
* [`css/highlightjs.min.css`](css/highlightjs.min.css) &mdash; The default theme uses the `github-dark` code highlighting style. Override this file to use a different `highlight.js` code highlighting style.
* [`css/highlightjs-copy.min.css`](css/highlightjs.min.css) &mdash; *...*
* [`js/theme.js`](js/theme.js) &mdash; Copy and override this file in order to add custom scripting.
* [`js/highlightjs.min.js`](js/highlightjs.min.js) &mdash; The default theme uses the default supported languages with `highlight.js`. Override this file to support a different set of programming languages.
* [`js/highlightjs-copy.min.js`](js/highlightjs-copy.min.js)
