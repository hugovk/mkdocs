import base64
import io
import json
import pathlib
import posixpath
import typing
import zipfile

import httpx
import flask
import jinja2
import markdown
import tomllib
import importlib.resources

from .extensions.rewrite_urls import PageContext


# Config...

class Config:
    def __init__(self, config: dict, filename: str) -> None:
        self._config = config
        self._filename = filename

    def get(self, *args: str):
        value = self._config
        for arg in args:
            if not isinstance(value, dict) or arg not in value:
                return None
            value = value[arg]
        return value

    def __getitem__(self, key: str) -> typing.Any:
        return self._config[key]

    def __repr__(self):
        return f'<Config {self._filename!r}>'


class ConfigError(Exception):
    pass


class Page:
    def __init__(self, text: str, html: str, toc: str, title: str, url: str, path: str):
        self.text = text  # The markdown text
        self.html = html  # The rendered html
        self.toc = toc    # The HTML table of contents
        self.title = title
        self.url = url
        self.path = path


class Nav:
    def __init__(self, html: str, current, previous, next):
        self.html = html  # The HTML nav menu
        self.current = current
        self.previous = previous
        self.next = next


# Handlers...

class Handler:
    """
    The base interface for loading resources.
    """

    def load_paths(self) -> list[pathlib.Path]:
        """
        Load a list of all the resource paths that this handler provides.
        """
        return []

    def read(self, path: pathlib.Path) -> bytes:
        """
        Load the resource content given it's path.
        """
        return ''


class Directory(Handler):
    """
    A handler for loading resources from the local filesystem.
    """

    def __init__(self, dir: pathlib.Path | None = None) -> None:
        self._dir = pathlib.Path.cwd() if dir is None else pathlib.Path(dir)
        self._dir_repr = '[CWD]' if dir is None else f"{dir!r}"

    def load_paths(self) -> list[pathlib.Path]:
        return sorted([
            f.relative_to(self._dir)
            for f in self._dir.rglob("[!.]*")
            if f.is_file()
        ])

    def read(self, path: pathlib.Path) -> bytes:
        return self._dir.joinpath(path).read_bytes()

    def __repr__(self):
        return f'<Directory {self._dir_repr}>'


class Package(Handler):
    """
    A handler for loading resources from a python package.
    """

    def __init__(self, pkg_dir: str = 'mkdocs:theme') -> None:
        pkg, _, dir = pkg_dir.partition(':')
        self._files = importlib.resources.files(pkg).joinpath(dir)

    def _load_paths(self, subdir: str) -> list[pathlib.Path]:
        files = []
        for entry in self._files.joinpath(subdir).iterdir():
            if entry.is_file():
                f = pathlib.Path(subdir).joinpath(entry.name)
                files.append(f)
            elif entry.is_dir():
                d = pathlib.Path(subdir).joinpath(entry.name)
                for f in self._load_paths(d):
                    files.append(f)
        return files

    def load_paths(self) -> list[pathlib.Path]:
        return sorted(self._load_paths(subdir=''))

    def read(self, path: pathlib.Path) -> bytes:
        return self._files.joinpath(path).read_bytes()

    def __repr__(self):
        return f'<Package {self._pkg!r}>'


class ZipURL(Handler):
    def __init__(self, url: str) -> None:
        self._url = url
        self._topdir = ''

    def load_paths(self) -> list[pathlib.Path]:
        r = httpx.get(self._url, follow_redirects=True)
        r.raise_for_status()
        b = io.BytesIO(r.content)
        with zipfile.ZipFile(b, 'r') as zip_ref:
            names = [
                pathlib.PosixPath(name) for name in zip_ref.namelist()
                if not name.endswith('/')
            ]
            if len(set([name.parts[0] for name in names])) == 1:
                self._topdir = names[0].parts[0]
                names = [pathlib.PosixPath(*name.parts[1:]) for name in names]
        return names

    def read(self, path: pathlib.Path) -> bytes:
        r = httpx.get(self._url, follow_redirects=True)
        r.raise_for_status()
        b = io.BytesIO(r.content)
        with zipfile.ZipFile(b, 'r') as zip_ref:
            path = f"{self._topdir}/{path}" if self._topdir else path
            with zip_ref.open(str(path)) as f:
                return f.read()


# Resources & Templates...

class Resource:
    def __init__(self, path: pathlib.Path, url: str, handler: Handler) -> None:
        self.path = path
        self.url = url
        self.handler = handler

    @property
    def output_path(self) -> pathlib.Path:
        if self.url.endswith('/'):
            return pathlib.Path(self.url.lstrip('/')).joinpath('index.html')
        return pathlib.Path(self.url.lstrip('/'))

    def read(self) -> bytes:
        return self.handler.read(self.path)

    def __repr__(self) -> str:
        return f'<Resource {self.url!r} {self.path.as_posix()!r}>'


class Template:
    def __init__(self, name: str, path: pathlib.Path, handler: Handler) -> None:
        self.name = name
        self.path = path
        self.handler = handler

    def read(self) -> bytes:
        return self.handler.read(self.path)

    def __repr__(self) -> str:
        return f'<Template {self.name!r}>'


###############################################################################
# Jinja2 configuration...

@jinja2.pass_context
def url(ctx, url_to):
    """
    The 'url' filter is used in HTML templates to ensure that
    static media is referenced relative to the active page.

    Example usage:

    <link rel="stylesheet" href="{{ '/css/theme.css' | url }}">

    The resulting link will be a relative link, allowing sites to
    be deployed either at the root domain Eg. `https://www.example.com/`,
    or on a subdirectory. Eg. `https://www.example.com/project/`
    """
    url_from = ctx['page'].url
    url_rel = posixpath.relpath(url_to, url_from)
    return url_rel


class TemplateLoader(jinja2.BaseLoader):
    """
    A Jinja2 template loader that uses whichever Templates are
    loaded by the MkDocs configuration.
    """
    def __init__(self, templates: list[Template]):
        self.templates = templates

    def uptodate(self):
        return False

    def get_source(self, environment: jinja2.Environment, template: str):
        for t in self.templates:
            if t.name == template:
                source = t.read().decode('utf-8')
                return source, t.path, self.uptodate
        raise jinja2.TemplateNotFound(template)



###############################################################################
# Here we go...

class MkDocs:
    def __init__(self):
        self.config = self.load_config('mkdocs.toml')
        self.handlers = self.load_handlers(self.config)
        self.resources, self.templates = self.load_resources(self.handlers)
        self.env = self.load_env(self.templates)
        self.md = self.load_md(self.config)

    def path_to_url(self, path: pathlib.Path) -> str:
        if str(path).lower() in ('readme.md', 'index.md', 'index.html'):
            # 'README.md' -> '/'
            # 'index.html' -> '/'
            return pathlib.Path('/').joinpath(path).parent.as_posix().lower()
        if path.name.lower() in ('readme.md', 'index.md', 'index.html'):
            # 'topics/README.md' -> '/topics/'
            # 'topics/index.html' -> '/topics/'
            return pathlib.Path('/').joinpath(path).parent.as_posix().lower() + '/'
        elif path.suffix == '.md':
            # 'quickstart.md' -> '/quickstart/'
            # 'topics/installation.md' -> '/topics/installation/'
            return pathlib.Path('/').joinpath(path).with_suffix('').as_posix().lower() + '/'
        # 'css/styles.css' -> '/css/styles.css'
        return pathlib.Path('/').joinpath(path).as_posix()

    def load_config(self, filename: str) -> dict:
        path = pathlib.Path(filename)
        if not path.exists():
            print("* No 'config.toml' file, using defaults.")
            config = {}
            # raise ConfigError(f"Missing config '{filename}'")
        else:
            text = path.read_text()
            try:
                config = tomllib.loads(text)
            except tomllib.TOMLDecodeError as exc:
                raise ConfigError(f"Invalid TOML in config '{filename}'\n{exc}")

        default = {
            'mkdocs': {
                'nav': [],
                'resources': [
                    {'package': 'mkdocs:theme'},
                    {'directory': 'docs'},
                ],
            },
            'context': {
            },
            'markdown': {
                'extensions': [
                    'fenced_code',
                    'footnotes',
                    'tables',
                    'toc',
                    # 'pymdownx.tasklist',
                    # 'gfm_admonition',
                    'mkdocs.extensions.rewrite_urls',
                    'mkdocs.extensions.short_codes',
                    'mkdocs.extensions.strike_thru',
                ],
                'configs': {
                    'footnotes': {'BACKLINK_TITLE': ''},
                    'toc': {'anchorlink': True, 'marker': ''}
                },
            },
        }
        for key, value in default.items():
            if key not in config:
                config[key] = value
        return Config(config, filename=filename)

    def load_handlers(self, config: dict) -> list[Handler]:
        handlers = []
        for handler in config['mkdocs']['resources']:
            if len(handler) != 1:
                raise ConfigError("Misconfigured 'resources' section.")
            key = list(handler.keys())[0]
            value = list(handler.values())[0]
            if key == 'url':
                handlers.append(ZipURL(value))
            elif key == 'package':
                handlers.append(Package(value))
            elif key == 'directory':
                handlers.append(Directory(value))
        return handlers

        # return [
        #     # ZipURL('https://codeload.github.com/lovelydinosaur/test/zip/refs/tags/v2'),
        #     ZipURL('https://codeload.github.com/lovelydinosaur/test/zip/refs/heads/main'),
        #     # Package('mkdocs'),
        #     # ZipURL('https://github.com/lovelydinosaur/test/archive/refs/heads/main.zip'),
        #     Directory('docs'),
        # ]

    def load_resources(self, handlers: list[Handler]) -> tuple[list[Resource], list[Template]]:
        resources = {}
        templates = {}
        for handler in handlers:
            for path in handler.load_paths():
                if path.parts[0] == 'templates':
                    name = str(pathlib.Path(*path.parts[1:]))
                    templates[path] = Template(name, path, handler)
                else:
                    url = self.path_to_url(path)
                    resources[path] = Resource(path, url, handler)
        return (list(resources.values()), list(templates.values()))

    def load_env(self, templates: list[Template]) -> jinja2.Environment:
        loader = TemplateLoader(templates)
        env = jinja2.Environment(loader=loader, auto_reload=True)
        env.filters['url'] = url
        return env

    def load_md(self, config) -> markdown.Markdown:
        return markdown.Markdown(
            extensions=config['markdown']['extensions'],
            extension_configs=config['markdown']['configs']
        )

    def nav_lines(self, nav: dict, indent="") -> list[str]:
        lines = []
        for elem in nav:
            if 'path' in elem:
                lines.append(f'{indent}* [{elem['title']}]({elem['path']})')
            else:
                lines.append(f'{indent}* {elem['title']}')
            if 'children' in elem:
                sub_lines = self.nav_lines(elem['children'], indent + "    ")
                lines.extend(sub_lines)
        return lines

    def render(self, resource: Resource) -> bytes:
        if resource.path.suffix == '.md':
            mapping = {resource.path: resource.url for resource in self.resources}
            with PageContext(resource.path, mapping, relative=False) as ctx:
                nav_config = self.config['mkdocs'].get('nav', [])
                nav_lines = self.nav_lines(nav_config)
                nav_text = '\n'.join(nav_lines)
                nav_html = self.md.reset().convert(nav_text)
                nav = Nav(html=nav_html, current=ctx.current, previous=ctx.previous, next=ctx.next)
            with PageContext(resource.path, mapping, relative=True):
                text = resource.read().decode('utf-8')
                html = self.md.reset().convert(text)
                title = self.md.toc_tokens[0]['name'] if self.md.toc_tokens else ''
                page = Page(text=text, html=html, toc=self.md.toc, title=title, url=resource.url, path=resource.path)
            base = self.env.get_template('base.html')
            return base.render(page=page, nav=nav, config=self.config).encode('utf-8')
        return resource.read()
