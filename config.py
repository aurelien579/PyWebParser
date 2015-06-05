import xml.etree.ElementTree as ET
from core import *

class Config:
    
    def __init__(self, path):
        self.models = []
        self.load_config(path)
        
    def load_config(self, path):
        tree = ET.parse(path)
        root = tree.getroot()        
        self.load_and_add_models(root)
                
    def load_and_add_models(self, root):
        for node in root.findall('model'):
            self.add_model(node) 
            
    def add_model(self, node):
        model = Model(node.attrib['url'], node.attrib['name'])
        model.fields = self.load_fields(node)
        self.models.append(model)
    
    def load_fields(self, model_node):
        return [self.create_field(node) for node in model_node.findall('field')]
    
    def create_field(self, node):
        name = node.attrib['name']
        parser = eval(node.attrib['parser'])
        xpath = node.attrib['xpath']
        return Field(name, parser, xpath)
