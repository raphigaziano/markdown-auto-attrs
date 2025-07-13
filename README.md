# markdown\_auto\_attrs

A [Python-Markdown](https://github.com/Python-Markdown/markdown) extension to
automatically add some attributes to specific generated element.

## Install

```bash
python3 -m pip install markdown-auto-attrs
```

## Usage

```python
import markdown

s = '![alt text](/link/to/img.png)'
extensions = ['markdown_auto_attrs', ]
extension_configs = {
    'markdown_auto_attrs': {
        'element_attrs': {
            'img': {
                'loading': 'lazy',
                'class': 'my-class',
            }
        }
    },
}

print(markdown.markdown(s, extensions=extensions, extension_configs=extension_configs))
```

Output:

```html
<p><img src="/link/to/img.png" loading="lazy" class="my-class" /></p>
```

You can also `import` manually:

```python
import markdown
from markdown_auto_attrs import AutoAttrsExtension

s = '[example](https://example.com/)'

# with config
print(markdown.markdown(
  s, extensions=[AutoAttrsExtension(element_attrs={'a': {'target': '_blank'}})]
))
```

Output:

```html
<p><a href="https://example.com/" target="_blank">example</a></p>
```

For more information, see [Extensions - Python-Markdown documentation](https://python-markdown.github.io/extensions/)
and [Using Markdown as a Python Library - Python-Markdown documentation](https://python-markdown.github.io/reference/#extensions).

### CLI

```bash
python3 -m markdown -x markdown_auto_attrs input.md > output.html
python3 -m markdown -x markdown_auto_attrs -c config.json input.md > output.html
```

For more information, see [Using Python-Markdown on the Command Line - Python-Markdown documentation](https://python-markdown.github.io/cli/).

### Pelican

[Pelican](https://blog.getpelican.com/) is a static site generator.

Edit `pelicanconf.py`, `MARKDOWN` dict variable. Example:

```python
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'linenums': False,
            'guess_lang': False,
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {},

        'markdown_auto_attrs': {
          'element_attrs': {
              'img': {
                  'loading': 'lazy',
              },
          },
        },
    },
    'output_format': 'html5',
}
```

For more information, see [Settings - Pelican Docs](https://docs.getpelican.com/en/stable/settings.html).

## Options

By default, this extension does NOT do anything. the only configuration option
it accepts is a dict mapping alement tag names to another dict defining which
attributes will be set and their value.

## Roadmap

Initial release aims to stay as dumb as possible to solve an immediate need.
Matching *all* element of a given tag type isn't that useful though, so future
releases should add the possibility to assign callables in order to dynamically
decide whether or not an attribute should be set.
