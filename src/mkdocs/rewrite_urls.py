import contextvars
import markdown
import httpx
import os
import pathlib
import posixpath


page_context = contextvars.ContextVar('page_context')


def joinpath(x: pathlib.Path, y: pathlib.Path):
    return pathlib.Path(os.path.normpath(x.joinpath(y)))

class PageContext:
    def __init__(self, path: pathlib.Path, path_to_url: dict[pathlib.Path, str], relative: bool):
        self.path = path
        self.path_to_url = path_to_url
        self.url_to_path = {u: p for p, u in path_to_url.items()}
        self.relative = relative

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
            # We want to rewrite image and links.
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
                # We want to rewrite relative links... '/page'
                # We don't want to rewrite external links. 'https://elsewhere.com/here'
                # We don't want to rewrite anchor links. '#section'
                if url.is_relative_url and url._uri_reference.path:
                    link = pathlib.PosixPath(url.path)

                    # Path to the current page...
                    from_path = ctx.path
                    # Path to the linked page...
                    to_path = joinpath(ctx.path.parent, link) if ctx.relative else link
                    # Current URL...
                    from_url = ctx.path_to_url[from_path]
                    # Linked URL...
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

                    # Is this is a link to the current page?
                    if from_url == to_url:
                        el.set('class', 'active')
                        idx = len(links)

        # We also want to track the previous and next link.
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
