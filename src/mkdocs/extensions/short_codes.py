import markdown.inlinepatterns
import xml.etree.ElementTree as etree


codes = {
    '+1': '👍🏼',
    '-1': '👎',
    'smile': '😀',
    'heart': '❤️',
    'tada': '🎉',
    'fire': '🔥',
    'rocket': '🚀',
    'bug': '🐛',
    'thinking': '🤔',
    'eyes': '👀',
    'shipit': '🚢',
}


class ShortCodes(markdown.inlinepatterns.InlineProcessor):
    def handleMatch(self, m, data):
        code = m.group(1)
        emoji = codes.get(code)
        if emoji is None:
            return None, None, None
        el = etree.Element('span')
        el.text = emoji
        return el, m.start(0), m.end(0)
    

class ShortCodesExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md):
        pattern = r':([a-z]{3,10}|\+1|\-1):'
        processor = ShortCodes(pattern, md)
        md.inlinePatterns.register(processor, 'short_codes', 175)


def makeExtension(**kwargs):
    return ShortCodesExtension(**kwargs)
