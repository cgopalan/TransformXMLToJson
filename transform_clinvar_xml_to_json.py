"""
    Transforms an XML file of ReferenceClinVarAssertion objects to
    a JSON file.

    Input to the program:
    1. Full path of the source xml file that you want to read from.
    2. Full path of the json file that you want to create.

"""

import sys
import json
import xml.etree.cElementTree as ET


def do_transform(xml_file):
    """ Process the XML file as a stream and yield a json. """
    """ TODO: Use better variable names for loops. """
    for event, element in ET.iterparse(xml_file):
        if event == 'end':
            if element.tag == 'ClinVarSet':
                for x in element:
                    if x.tag == 'Title':
                        title = x.text
                    if x.tag == 'ReferenceClinVarAssertion':
                        for y in x:
                            if y.tag == 'ClinVarAccession':
                                acc = y.attrib['Acc']
                                version = int(y.attrib['Version'])
                            if y.tag == 'ClinicalSignificance':
                                for z in y:
                                    if z.tag == 'Description':
                                        desc = z.text
                            if y.tag == 'MeasureSet':
                                for z in y:
                                    if z.tag == 'Measure':
                                        m_type = z.attrib['Type']
                                        for a in z:
                                            if a.tag == 'Name':
                                                for b in a:
                                                    if b.tag == 'ElementValue':
                                                        p_name = b.attrib['Type']
                                            if a.tag == 'AttributeSet':
                                                hgvs_list = []
                                                for b in a:
                                                    if b.tag == 'Attribute' and 'HGVS' in b.attrib['Type']:
                                                        hgvs_list.append(b.text)
                # Yield the JSON string.
                yield make_json(title, acc, version, p_name, m_type, desc, hgvs_list)


def make_json(title, acc, version, p_name, m_type, desc, hgvs_list):
    """ Create a json string to be written to file. """
    output_dict = {
                    'rcvaccession': acc,
                    'rcvaccession_version': version,
                    'title': title,
                    'preferred_name': p_name,
                    'hgvs': hgvs_list,
                    'type': m_type,
                    'clinical_significance': desc
    }
    return json.dumps(output_dict)


def transform_clinvar(xml_file, json_file):
    """ Transform xml objects to json and write to file. """
    with open(json_file, 'a') as f:
        for json_rec in do_transform(xml_file):
            f.write(json_rec + '\n')

if __name__ == '__main__':
    transform_clinvar(sys.argv[1], sys.argv[2])
