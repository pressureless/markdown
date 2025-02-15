"""
Meta Data Extension for Python-Markdown
=======================================

This extension adds Meta Data handling to markdown.

See <https://Python-Markdown.github.io/extensions/meta_data>
for documentation.

Original code Copyright 2007-2008 [Waylan Limberg](http://achinghead.com).

All changes Copyright 2008-2014 The Python Markdown Project

License: [BSD](https://opensource.org/licenses/bsd-license.php)

"""

from . import Extension
from ..preprocessors import Preprocessor
import re
import logging
import yaml

log = logging.getLogger('MARKDOWN')

# Global Vars
META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')
META_MORE_RE = re.compile(r'^[ ]{4,}(?P<value>.*)')
BEGIN_RE = re.compile(r'^-{3}(\s.*)?')
END_RE = re.compile(r'^(-{3}|\.{3})(\s.*)?')


class MetaExtension (Extension):
    """ Meta-Data extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Add MetaPreprocessor to Markdown instance. """
        md.registerExtension(self)
        self.md = md
        md.preprocessors.register(MetaPreprocessor(md), 'meta', 27)

    def reset(self):
        self.md.Meta = {}


class MetaPreprocessor(Preprocessor):
    """ Get Meta-Data. """

    def run(self, lines, **kwargs):
        """ Parse Meta-Data and store in Markdown.Meta. """
        meta_lines, lines = self.split_by_meta_and_content(lines)
        meta = yaml.load("\n".join(meta_lines), Loader=yaml.FullLoader)
        self.md.Meta = meta if meta is not None else {}
        # meta = {}
        # key = None
        # if lines and BEGIN_RE.match(lines[0]):
        #     lines.pop(0)
        # while lines:
        #     line = lines.pop(0)
        #     m1 = META_RE.match(line)
        #     if line.strip() == '' or END_RE.match(line):
        #         break  # blank line or end of YAML header - done
        #     if m1:
        #         key = m1.group('key').lower().strip()
        #         value = m1.group('value').strip()
        #         try:
        #             meta[key].append(value)
        #         except KeyError:
        #             meta[key] = [value]
        #     else:
        #         m2 = META_MORE_RE.match(line)
        #         if m2 and key:
        #             # Add another line to existing key
        #             meta[key].append(m2.group('value').strip())
        #         else:
        #             lines.insert(0, line)
        #             break  # no meta data - done
        # self.md.Meta = meta
        return lines

    def split_by_meta_and_content(self, lines):
        meta_lines = []
        if lines[0] != "---":
            return meta_lines, lines
        lines.pop(0)
        for line in lines:
            if line in ("---", "..."):
                content_starts_at = lines.index(line) + 1
                lines = lines[content_starts_at:]
                break
            meta_lines.append(line)
        return meta_lines, lines


def makeExtension(**kwargs):  # pragma: no cover
    return MetaExtension(**kwargs)
