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
                self.process_element(child, attrs)
            self.process_tree(child)

    def process_element(self, element, attrs):
        for k, v in attrs.items():
            self.set_attr(element, k, v)

    def set_attr(self, element, attr_name, attr_val):
        local_attr = element.get(attr_name)
        if local_attr == self.ignore_value:
            del element.attrib[attr_name]
            return
        if not local_attr:
            element.set(attr_name, attr_val)


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
