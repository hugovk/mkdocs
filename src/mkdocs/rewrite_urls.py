import contextvars
import markdown
import posixpath
import httpx
import pathlib


page_context = contextvars.ContextVar('page_context')


class PageContext:
    def __init__(self, path: pathlib.Path, path_to_url: dict[pathlib.Path, str]):
        self.path = path
        self.path_to_url = path_to_url
        self.url_to_path = {u: p for p, u in path_to_url.items()}

    def __enter__(self):
        self._token = page_context.set(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        page_context.reset(self._token)


class URLProcessor(markdown.treeprocessors.Treeprocessor):
    def run(self, root):
        ctx = page_context.get()
        links = []
        idx = 0
        key = ''
        link = ''

        for el in root.iter():
            if el.tag == 'a':
                key = 'href'
                link = el.get(key)
            elif el.tag == 'img':
                key = 'src'
                link = el.get(key)
            else:
                key = ''
                link = ''

            if link:
                url = httpx.URL(link)
                if url.is_relative_url and url._uri_reference.path:
                    from_path = ctx.path
                    to_path = ctx.path.parent.joinpath(url.path)
                    from_url = ctx.path_to_url[from_path]
                    to_url =  ctx.path_to_url.get(to_path)
                    if to_url is None:
                        continue
                    rewrite = posixpath.relpath(to_url, from_url)
                    if to_url.endswith('/') and rewrite != '.':
                        rewrite += '/'
                    if url.query:
                        rewrite += f'?{url.query}'
                    if url.fragment:
                        rewrite += f'#{url.fragment}'
                    el.set(key, rewrite)
                    links.append({"title": el.text, "url": rewrite})

                    if from_url == to_url:
                        el.set('class', 'active')
                        idx = len(links)

        links = [None] + links + [None]
        if idx is not None:
            ctx.previous = links[idx - 1]
            ctx.current = links[idx]
            ctx.next = links[idx + 1]


class RewriteURLs(markdown.extensions.Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(URLProcessor(md), 'rewrite_urls', 15)


def makeExtension(**kwargs):
    return RewriteURLs(**kwargs)
