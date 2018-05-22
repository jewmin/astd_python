# -*- coding: utf-8 -*-
# xml解析器
try:
    import xml.etree.cElementTree as Et
except ImportError:
    import xml.etree.ElementTree as Et


class XmlParse(object):
    def __init__(self, coding='UTF-8'):
        self._coding = coding

    def _parse_node(self, node):
        tree = {}

        # Save childrens
        for child in node.getchildren():
            ctag = child.tag
            ctext = child.text.strip().encode(self._coding) if child.text is not None else ''
            ctree = self._parse_node(child)

            if not ctree:
                cdict = self._make_dict(ctag, ctext)
            else:
                cdict = self._make_dict(ctag, ctree)

            if ctag not in tree:  # First time found
                tree.update(cdict)
                continue

            atree = tree[ctag]
            if not isinstance(atree, list):
                tree[ctag] = [atree]  # Multi entries, change to list

            if not ctree:
                tree[ctag].append(ctext)
            else:
                tree[ctag].append(ctree)

        return tree

    @staticmethod
    def _make_dict(tag, value):
        """Generate a new dict with tag and value

        """
        ret = {tag: value}

        return ret

    def parse(self, xml):
        """Parse xml string to python dict

        """
        el = Et.fromstring(xml)

        ctree = self._parse_node(el)

        if not ctree:
            cdict = self._make_dict(el.tag, el.text)
        else:
            cdict = self._make_dict(el.tag, ctree)

        return cdict

    def parse_file(self, xml_file):
        """Parse xml file to python dict

        """
        el = Et.ElementTree(file=xml_file).getroot()

        ctree = self._parse_node(el)

        if not ctree:
            cdict = self._make_dict(el.tag, el.text)
        else:
            cdict = self._make_dict(el.tag, ctree)

        return cdict
