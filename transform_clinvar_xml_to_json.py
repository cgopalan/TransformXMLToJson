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
    for event, element in ET.iterparse(xml_file):
        if event == 'end' and element.tag == 'ClinVarSet':
            # initialize vars
            title, acc, version, p_name, m_type, desc = '', '', '', '', '', ''
            hgvs_list = None

            e_title = element.find('./Title')
            if e_title is not None:
                title = e_title.text

            e_clinvaracc = element.find('./ReferenceClinVarAssertion/ClinVarAccession')
            if e_clinvaracc is not None:
                acc = e_clinvaracc.attrib['Acc']
                version = int(e_clinvaracc.attrib['Version']) if e_clinvaracc.attrib['Version'] else ''

            e_elemval = element.find('./ReferenceClinVarAssertion/MeasureSet/Measure/Name/ElementValue')
            if e_elemval is not None:
                p_name = e_elemval.attrib['Type']

            e_hgvs = element.findall('./ReferenceClinVarAssertion/MeasureSet/Measure/AttributeSet/Attribute')
            if e_hgvs is not None:
                hgvs_list = [x.text for x in e_hgvs if 'HGVS' in x.attrib['Type']]

            e_type = element.find('./ReferenceClinVarAssertion/MeasureSet/Measure')
            if e_type is not None:
                m_type = e_type.attrib['Type']

            e_clinsig = element.find('./ReferenceClinVarAssertion/ClinicalSignificance/Description')
            if e_clinsig is not None:
                desc = e_clinsig.text

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
