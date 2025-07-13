import os
import sys
import unittest

import markdown


class BaseTestCase(unittest.TestCase):

    def md(self, source, **config):
        if 'element_attrs' not in config:
            config = {'element_attrs': config}
        md = markdown.Markdown(
            # extra extension is bundled by default with python-markdown and
            # will simplify testing manually set attributes.
            extensions=['extra', 'auto-attrs'],
            extension_configs={
                'auto-attrs': config,
            })
        return md.convert(source)


class TestAutoAttrs(BaseTestCase):

    def test_base(self):
        result = self.md('Lorem Ipsum', p={'class': 'auto-generated'})
        self.assertEqual(
            result, '<p class="auto-generated">Lorem Ipsum</p>')

    def test_no_config_is_a_noop(self):
        result = self.md('Here\'s a [link](http://site.com) to somewhere')
        self.assertEqual(
            result,
            '<p>Here\'s a <a href="http://site.com">link</a> to somewhere</p>')

    def test_multiple_instances_of_the_same_tag(self):
        result = self.md(
            '[link name](http://foo.com)'
            '[another link](http://bar.com)',
            a={'title': 'wee'})
        self.assertIn(
            '<a href="http://foo.com" title="wee">link name</a>', result)
        self.assertIn(
            '<a href="http://bar.com" title="wee">another link</a>', result)

    def test_several_tag_types(self):
        result = self.md(
            '[link name](http://site.com)'
            '![alt text](/link/to/img.png)',
            a={'title': 'wee'},
            img={'loading': 'lazy'})
        self.assertIn(
            '<a href="http://site.com" title="wee">link name</a>', result)
        self.assertIn(
            '<img alt="alt text" loading="lazy" src="/link/to/img.png" />',
            result)

    def test_attr_overides(self):
        result = self.md(
            '[link name](http://url.net "local")', a={'title': 'global'})
        self.assertIn(
            '<a href="http://url.net" title="local">link name</a>', result)

    def test_auto_attr_ignore(self):
        result = self.md(
            '**strong**{class="__auto_attrs_ignore"}',
            strong={'class': 'should-be-ignored'})
        self.assertIn('<strong>strong</strong>', result)

    def test_auto_attr_ignore_custom_value(self):
        result = self.md(
            '# title {title="custom-ignore-value"}',
            element_attrs={'h1': {'title': 'global-title'}},
            ignore_value='custom-ignore-value')
        self.assertIn('<h1>title</h1', result)


def importable_callback(e, md):
    if 'cats' in e.get('src'):
        e.set('class', 'kitty')


class TestAutoAttrsCallbacks(BaseTestCase):

    def setUp(self):
        # Add test dir to the path to be able to import stuff from it.
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))

    def test_callable(self):

        def callback(e, md):
            alt = e.get('alt')
            e.set('alt', alt.upper())

        result = self.md(
            '![alt](/path/to/img.jpg)', img=callback)
        self.assertIn('<img alt="ALT" src="/path/to/img.jpg" />', result)

    def test_dynamic_callable_import(self):
        result = self.md(
            '![alt](/path/to/cats/img.jpg)',
            img='tests.test_auto_attrs.importable_callback')
        self.assertIn(
            '<img alt="alt" class="kitty" src="/path/to/cats/img.jpg" />',
            result)
