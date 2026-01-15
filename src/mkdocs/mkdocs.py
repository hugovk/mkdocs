import pathlib
import posixpath
import typing

import httpx
import jinja2
import markdown
import tomllib
import importlib.resources

from .rewrite_urls import PageContext


@jinja2.pass_context
def url(ctx, url_to):
    url_from = ctx['resource'].url
    url_rel = posixpath.relpath(url_to, url_from)
    return url_rel


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

    def __init__(self, pkg: str = 'mkdocs') -> None:
        self._pkg = pkg
        self._files = importlib.resources.files(pkg).joinpath('theme')

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


# class ZipURL(Handler):
#     def __init__(self, url: str) -> None:
#         self._url = url
#         self._topdir = ''

#     def load_paths(self) -> list[pathlib.Path]:
#         r = httpx.get(self._url)
#         b = io.BytesIO(r.body)
#         with zipfile.ZipFile(b, 'r') as zip_ref:
#             names = [
#                 pathlib.PosixPath(name) for name in zip_ref.namelist()
#                 if not name.endswith('/')
#             ]
#             if len(set([name.parts[0] for name in names])) == 1:
#                 self._topdir = names[0].parts[0]
#                 names = [pathlib.PosixPath(*name.parts[1:]) for name in names]
#         return names

#     def read(self, path: pathlib.Path) -> bytes:
#         r = httpx.get(self._url)
#         b = io.BytesIO(r.body)
#         with zipfile.ZipFile(b, 'r') as zip_ref:
#             path = f"{self._topdir}/{path}" if self._topdir else path
#             with zip_ref.open(str(path)) as f:
#                 return f.read()

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


class TemplateLoader(jinja2.BaseLoader):
    def __init__(self, templates: list[Template]):
        self.templates = templates

    def get_source(self, environment, template: str):
        for t in self.templates:
            if t.name == template:
                source = t.read().decode('utf-8')
                return source, t.path, None
        raise jinja2.TemplateNotFound(template)


class MkDocs:
    def __init__(self, config: str = '', theme: str = ''):
        self.config = config or 'mkdocs.toml'
        self.theme = theme
        self.content_types = {
            ".json": "application/json",
            ".js": "application/javascript",
            ".html": "text/html",
            ".css": "text/css",
            ".png": "image/png",
            ".jpeg": "image/jpeg",
            ".jpg": "image/jpeg",
            ".gif": "image/gif",
        }

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
            raise ConfigError(f"Missing config '{filename}'")

        text = path.read_text()
        try:
            config = tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            raise ConfigError(f"Invalid TOML in config '{filename}'\n{exc}")

        # if 'mkdocs' not in config:
        #     raise ConfigError(f"Config '{filename}' missing '[mkdocs]' section.")
        # if 'version' not in config['mkdocs']:
        #     raise ConfigError(f"Config '{filename}' missing 'version=...' in '[mkdocs]' section.")
        # if config['mkdocs']['version'] != 2:
        #     raise ConfigError(f"Config '{filename}' expected 'version=2' in '[mkdocs]' section.")

        default = {
            'mkdocs': {
                'version': 2
            },
            'site': {
                'title': 'MkDocs',
                'favicon': '📘',
                'nav': [],
            },
            # 'handlers': [
            #     {'type': 'mkdocs.Package', 'pkg': 'mkdocs:theme'}
            #     {'type': 'mkdocs.Directory', 'dir': 'docs'}
            # ],
            'markdown': {
                'extensions': [
                    'fenced_code',
                    'footnotes',
                    'tables',
                    'toc',
                    # 'pymdownx.tasklist',
                    # 'gfm_admonition',
                    'mkdocs.rewrite_urls',
                    'mkdocs.short_codes',
                    'mkdocs.strike_thru',
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
        if not pathlib.Path('docs').is_dir():
            return [
                Package('mkdocs'),
                Directory('.'),
            ]
        return [
            Package('mkdocs'),
            Directory('docs'),
        ]

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

    def render(self, resource: Resource, resources: list[Resource], config: dict, env: jinja2.Environment, md: markdown.Markdown) -> bytes:
        if resource.path.suffix == '.md':
            mapping = {resource.path: resource.url for resource in resources}
            with PageContext(resource.path, mapping, relative=False) as page:
                nav_lines = self.nav_lines(config['site']['nav'])
                nav_text = '\n'.join(nav_lines)
                nav_html = md.reset().convert(nav_text)
            with PageContext(resource.path, mapping, relative=True):
                page_text = resource.read().decode('utf-8')
                page_html = md.reset().convert(page_text)
            base = env.get_template('base.html')
            return base.render(content=page_html, nav=nav_html, toc=md.toc, config=config, page=page, resource=resource).encode('utf-8')
        return resource.read()

    # Commands...

    def build(self):
        """
        $ mkdocs build
        """
        config = self.load_config('mkdocs.toml')
        handlers = self.load_handlers(config)
        resources, templates = self.load_resources(handlers)
        env = self.load_env(templates)
        md = self.load_md(config)

        buildpath = pathlib.Path('site')
        for resource in resources:
            output = self.render(resource, resources, config, env, md)
            build_path = buildpath.joinpath(resource.output_path)
            build_path.parent.mkdir(parents=True, exist_ok=True)
            build_path.write_bytes(output)

    def serve(self):
        """
        $ mkdocs serve
        """
        config = self.load_config('mkdocs.toml')
        handlers = self.load_handlers(config)
        resources, templates = self.load_resources(handlers)
        env = self.load_env(templates)
        md = self.load_md(config)

        urls = {resource.url: resource for resource in resources}
        def app(request):
            path = request.url.path
            resource = urls.get(path)
            if resource is None:
                redirect = f"{path}/"
                if urls.get(redirect) is not None:
                    return httpx.Response(302, headers={'Location': redirect})
                not_found = httpx.Text('Not Found')
                return httpx.Response(404, content=not_found)
            content = self.render(resource, resources, config, env, md)
            content_type = self.content_types.get(resource.output_path.suffix)
            return httpx.Response(200, headers={'Content-Type': content_type}, content=content)

        httpx.run(app)
