# markdown\_auto\_attrs

A [Python-Markdown](https://github.com/Python-Markdown/markdown) extension to
automatically add some attributes to specific elements in the generated html
output.

## Install

From github:

```bash
python3 -m pip install git+https://github.com/raphigaziano/markdown-auto-attrs
```

## Usage

The quick and dumb way:

```python
import markdown

s = '![alt text](/link/to/img.png)'
extensions = ['auto-attrs']
extension_configs = {
    'auto-attrs': {
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
<p><img alt="alt text" src="/link/to/img.png" loading="lazy" class="my-class" /></p>
```

You can also `import` manually:

```python
import markdown
from markdown_auto_attrs import AutoAttrsExtension

s = '[exemple](https://exemple.com/)'

# with config
print(markdown.markdown(
    s, extensions=[AutoAttrsExtension(element_attrs={'a': {'target': '_blank'}})]
))
```

Output:

```html
<p><a href="https://exemple.com/" target="_blank">exemple</a></p>
```

For more information, see [Extensions - Python-Markdown documentation](https://python-markdown.github.io/extensions/)
and [Using Markdown as a Python Library - Python-Markdown documentation](https://python-markdown.github.io/reference/#extensions).

### CLI

```bash
python3 -m markdown -x auto-attrs input.md > output.html
python3 -m markdown -x auto-attrs -c config.json input.md > output.html
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

        'auto-attrs': {
            'element_attrs': {
                'img': { 'loading': 'lazy' },
            },
        },
    },
    'output_format': 'html5',
}
```

For more information, see [Settings - Pelican Docs](https://docs.getpelican.com/en/stable/settings.html).

## Callbacks

When using a static dictionnary to define which attributes should be added,
*every* matching tag in the generated output will have those attributes
set. This may be what you want, but you can also replace the attribute dict
with a reference to a callable to get a little more control:

```python
# callbacks.py
def my_callback(element, md):
    if 'cats' in e.get('src'):
        e.set('class', 'kitty')

# main.py
import markdown

my_other_callback(element, md):
    ...

s = '![alt text](/link/to/cats/img.png)'
extensions = ['auto-attrs']
extension_configs = {
    'auto-attrs': {
        'element_attrs': {
            'img': 'callbacks.my_callback',
            'a': my_other_callback,
        }
    },
}

print(markdown.markdown(s, extensions=extensions, extension_configs=extension_configs))
```

Output:

```html
<p><img alt="alt text" src="/link/to/cats/img.png" class="kitty" /></p>
```

Callbacks get passed the current element being processed, as well as an instance
of the running `Markdown` object, from which you can get access to the parser,
document root, etc.

## Overriding attributes

If an element already defines an attribute listed in the global mapping, then
the global value will be ignored and the "local" attribute will be left
untouched.

## Bypass attribute setting

Individual elements can also define a custom attribute value (`__auto_attrs_ignore`
by default) to bypass attribute replacement.

## Options

- `element_attrs`:

  A mapping of element tag names to either:

  - a dict of static attributes names and values (see the first exemple above).
  - a callable to dynamically alter the matched element.

- `ignore_value`:

  The attribute value that will bypass processing an element. defaults to
  `__auto_attrs_ignore`.

- `fail_silently`:

  log exceptions without raising them. Defaults to True. Disable for debugging.

## Roadmap

Some planned feature that I don't need right now but would be nice to have:

- xpath selectors to select elements
- handle list-like attributes (ie, class) to add to / remove from it rather
  than replace the whole attribute.

## Acknowledgments

- This README structure was stolen from
  [Phucker's markdown_link_attr_modifier](https://github.com/Phuker/markdown_link_attr_modifier/),
  which also served as a reference on the Markdown extension API.
