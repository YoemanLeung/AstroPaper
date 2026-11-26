#!/usr/bin/env python3
"""Pandoc JSON filter: color paper identifiers and authors only in PDF/LaTeX.

Learn author names from the documented ID + Author: title / Author et al.
entries, then recognize those names throughout the document. Explicit author
links to arXiv and compact Author+YYYY citations are also supported.
"""
import json
import re
import sys

ID = re.compile(r"(?:arXiv:)?\d{4}\.\d{4,5}(?:v\d+)?$")
BARE_ID = r"(?<![\w.])(?:arXiv:)?\d{4}\.\d{4,5}(?:v\d+)?(?![\w.])"
AUTHOR_YEAR = r"\b[A-Z][\w'-]+\+(?:19|20)\d{2}\b"
TEXT_TYPES = {"Str", "Space", "SoftBreak"}


def plain(node):
    if node['t'] == 'Str':
        return node['c']
    if node['t'] in {'Space', 'SoftBreak'}:
        return ' '
    return ''


def inline_lists(value):
    if isinstance(value, list):
        if value and all(isinstance(x, dict) and x.get('t') in
                         TEXT_TYPES | {'Link', 'Code', 'Emph', 'Strong',
                                       'Span', 'RawInline', 'Quoted', 'Math',
                                       'Cite', 'Note', 'LineBreak', 'Image',
                                       'Superscript', 'Subscript', 'Strikeout',
                                       'SmallCaps', 'Underline'} for x in value):
            yield value
        for item in value:
            yield from inline_lists(item)
    elif isinstance(value, dict):
        yield from inline_lists(value.get('c', []))


def author_names(document):
    names = set()
    for items in inline_lists(document['blocks']):
        first = items[0]
        if first['t'] != 'Link':
            continue
        label = ''.join(plain(x) for x in first['c'][1])
        if not ID.fullmatch(label):
            continue
        following = []
        for item in items[1:]:
            if item['t'] not in TEXT_TYPES:
                break
            following.append(plain(item))
        match = re.match(r'\s+([^:\n]{1,100}?)(?=:| et al\.)', ''.join(following))
        if match:
            name = match[1].strip()
            if not any(c.isdigit() for c in name):
                names.add(name)
    return names


def colored(items, color):
    if color == "paperauthor":
        items = [{"t": "Strong", "c": items}]
    return [{'t': 'RawInline', 'c': ['latex', r'\textcolor{' + color + '}{']},
            *items, {'t': 'RawInline', 'c': ['latex', '}']}]


def filter_document(document, target):
    if target not in {'latex', 'beamer'}:
        return document
    names = sorted(author_names(document), key=len, reverse=True)
    author_pattern = '|'.join(re.escape(n) for n in names)
    patterns = [BARE_ID, AUTHOR_YEAR]
    if author_pattern:
        patterns.append(r'(?<!\w)(?:' + author_pattern + r')(?!\w)')
    pattern = re.compile('|'.join(patterns))

    def text_run(items):
        text = ''.join(plain(x) for x in items)
        matches = list(pattern.finditer(text))
        if not matches:
            return items
        output, start = [], 0
        for match in matches:
            if match.start() > start:
                output.append({'t': 'Str', 'c': text[start:match.start()]})
            color = 'arxivid' if ID.fullmatch(match[0]) else 'paperauthor'
            output.extend(colored([{'t': 'Str', 'c': match[0]}], color))
            start = match.end()
        if start < len(text):
            output.append({'t': 'Str', 'c': text[start:]})
        return output

    def walk(value):
        if isinstance(value, dict):
            if value.get('t') == 'Link':
                attr, label, destination = value['c']
                text = ''.join(plain(x) for x in label)
                if ID.fullmatch(text):
                    label = colored(label, 'arxivid')
                elif re.match(r'https?://(?:www\.)?arxiv.org/abs/', destination[0]):
                    label = colored(label, 'paperauthor')
                else:
                    label = walk(label)
                return {'t': 'Link', 'c': [attr, label, destination]}
            # Code, math, URLs, and raw markup are never rewritten.
            if value.get('t') in {'Code', 'CodeBlock', 'Math', 'RawInline', 'RawBlock'}:
                return value
            return {k: walk(v) for k, v in value.items()}
        if not isinstance(value, list):
            return value
        result, run = [], []
        for item in value:
            if isinstance(item, dict) and item.get('t') in TEXT_TYPES:
                run.append(item)
            else:
                result.extend(text_run(run))
                run = []
                result.append(walk(item))
        result.extend(text_run(run))
        return result

    document['blocks'] = walk(document['blocks'])
    return document


if __name__ == '__main__':
    json.dump(filter_document(json.load(sys.stdin), sys.argv[1]), sys.stdout)
