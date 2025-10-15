# Styling

Styling is handled with HTML templating and regular web design.

## Templates

Markdown documents are rendered using Jinja templating.

The base template for rendering is `templates/base.html`:

```html
<html>
    <head>
        <meta charset="utf-8">
        <title>{{ config['site']['title'] }}</title>
        <link rel="icon" href="/img/favicon.svg">
        <link rel="stylesheet" href="/css/highlightjs.min.css">
        <link rel="stylesheet" href="/css/theme.css">
        <script src="/js/highlightjs.min.js"></script>
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
        </main>
    </body>
</html>
```

You can override this template locally and adapt it to make layout changes.

## Media assets

The default theme includes the following assets:

* `css/theme.css` &mdash; *Copy and overide this file in order to change the color palette, the typography, or to other style changes.*
* `css/highlightjs.min.css` &mdash; *The default theme uses the `github-dark` code highlighting style. Override this file to use a different `highlight.js` code highlighting style.*
* `js/theme.js` &mdash; *Copy and override this file in order to add custom scripting.*
* `js/highlightjs.min.js` &mdash; *The default theme uses the default supported languages with `highlight.js`. Override this file to support a different set of programming languages.*
