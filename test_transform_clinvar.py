import unittest
import xml.etree.cElementTree as ET

SOURCE_XML_FILE = 'ClinVarFull.xml'

OUTPUT_FILE = 'ClinVarFull.json'

class TransformClinvarTests(unittest.TestCase):
    """ Tests for transform. """

    def test_all_objects_transformed(self):
        """ Test that all the ReferenceClinVarAssertion objects were transformed. """
        num_xml_objects = count_xml_objects(SOURCE_XML_FILE)
        num_json_objects = count_json_objects(OUTPUT_FILE)
        print(num_xml_objects, num_json_objects)
        self.assertEqual(num_xml_objects, num_json_objects)


def count_xml_objects(xml_file):
    """ Count ReferenceClinVarAssertion objects in xml file. """
    count = 0
    for event, element in ET.iterparse(xml_file):
        #title, acc, version, m_type, desc = '', '', '', '', ''
        if event == 'end' and element.tag == 'ReferenceClinVarAssertion':
            count += 1
    return count


def count_json_objects(json_file):
    """ Count lines in json file. """
    return sum(1 for line in open(json_file))


if __name__ == '__main__':
    unittest.main()
