import unittest

import markdown


class TestAutoAttrs(unittest.TestCase):

    def md(self, source, **config):
        md = markdown.Markdown(
            extensions=['auto-attrs'],
            extension_configs={
                'auto-attrs': {'element_attrs': config}
            })
        return md.convert(source)

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
