import markdown.inlinepatterns
import xml.etree.ElementTree as etree


class StrikeThru(markdown.inlinepatterns.InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element('del')
        el.text = m.group(1)
        return el, m.start(0), m.end(0)

class StrikeThruExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md):
        pattern = r'~~([^~]+)~~'
        processor = StrikeThru(pattern, md)
        md.inlinePatterns.register(processor, 'strike_thru', 175)


def makeExtension(**kwargs):
    return StrikeThruExtension(**kwargs)
