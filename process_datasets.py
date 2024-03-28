import os
import sys
import xml.etree.ElementTree as ET


class DataProcess():

    def __init__(self, dataset_name: str, data_path: str) -> None:
        self.dataset_name = dataset_name
        self.data_path = data_path
        # Check dataset name.
        dataset_names = ['i2b2', 'mimiciv']
        if self.dataset_name not in dataset_names:
            sys.exit(f"Selected dataset name is not in {dataset_names}")
        self.text = ''
        self.sents = list()
        self.annotation = {}

        
    def parse_i2b2(self, file_name):
        tree = ET.parse(file_name)
        root = tree.getroot()
        
        for child in root:
            if child.tag == 'TEXT':
                self.text = child.text
                #self.sents = sent_tokenize(self.text)  # Avoiding sentence tokenization to facilitate comparison.
            if child.tag == 'TAGS':
                tags = child
                for tag_child in tags:
                    key = f"{tag_child.attrib['start']}-{tag_child.attrib['end']}"
                    self.annotation[key] = tag_child.attrib

    def parse_mimiciv(self):
        pass

    

if __name__ == '__main__':

    i2b2_path = '../datasets/i2b2/Track1-de-indentification/PHI/'
    mimiciv_path = '../datasets/mimic-iv-note-deidentified-free-text-clinical-notes-2.2/note/'

    DataProcess('i2b2', i2b2_path)
    print