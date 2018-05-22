# -*- coding: utf-8 -*-

from xml.etree import ElementTree as eTree


def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def get_webos_elem():
    key_tag = eTree.Element('key')

    type_tag = eTree.Element('type')
    type_tag.text = 'F'
    key_tag.append(type_tag)

    name_tag = eTree.Element('name')
    name_tag.text = 'mobileWebOs'
    key_tag.append(name_tag)

    description_tag = eTree.Element('description')
    description_tag.text = 'OS구분코드'
    key_tag.append(description_tag)

    return key_tag


if __name__ == "__main__":
    xml_files = ['D:/workspace_python/viewcache-editor/sample.xml', 'D:/workspace_python/viewcache-editor/sample2.xml',
                 'D:/workspace_python/viewcache-editor/sample3.xml']
    for xml_file in xml_files:
        with open(xml_file, 'rt', encoding='utf-8') as file:
            root = eTree.fromstring(file.read())
            for uri_element in root.iter('uri'):
                name_tags = uri_element.findall('./mappings/mapping/name')
                if not all('/ajax' in name_tag.text for name_tag in name_tags):
                    print([name_tag.text for name_tag in name_tags], sep=',', end='\n', flush=True)
                    keys_elem = uri_element.find('./keys')
                    keys_elem.append(get_webos_elem())

        indent(root)
        print(eTree.tostring(root, encoding="unicode"))  # utf-8로 인코딩시 return type은 string이 아니고 bytestring임.
        eTree.ElementTree(root).write(xml_file, encoding="utf-8")
