"""
Python markdown extension to set arbitrary attributes generated html elements.

Author: https://github.com/raphigaziano

"""
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class AutoAttrsTreeprocessor(Treeprocessor):

    def __init__(self, *args, **kwargs):
        self.element_attrs = kwargs.pop('element_attrs')
        self.ignore_value = kwargs.pop('ignore_value')
        super(AutoAttrsTreeprocessor, self).__init__(*args, **kwargs)

    def run(self, root):
        self.process_tree(root)

    def process_tree(self, parent):
        for child in parent:
            if (attrs := self.element_attrs.get(child.tag, None)):
                self.add_attrs(child, attrs)
            self.process_tree(child)

    def add_attrs(self, element, attrs):
        for k, v in attrs.items():
            local_attr = element.get(k)
            if local_attr == self.ignore_value:
                del element.attrib[k]
                continue
            if not local_attr:
                element.set(k, v)


class AutoAttrsExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'element_attrs': [{}, 'Attribute mapping.'],
            'ignore_value': [
                '__auto_attrs_ignore',
                'Attributes containing this value will be removed instead of '
                'being set to the global value provided in the '
                '`element_attrs` dict'
            ],
        }
        super(AutoAttrsExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
            AutoAttrsTreeprocessor(md, **self.getConfigs()),
            'auto_attrs',
            -9998
        )


def makeExtension(**kwargs):
    return AutoAttrsExtension(**kwargs)
