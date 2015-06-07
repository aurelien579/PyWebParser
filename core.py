import re
import requests
from lxml import html
import lxml
import xml.etree.ElementTree as ET

class Config:
    
    def __init__(self, path):
        self.models = []
        self.load_config(path)
        
    def load_config(self, path):
        root = ET.parse(path).getroot()
        for node in root.findall('page'):
            url = node.attrib['url']
            model = self.create_model(node.find('model'))
            self.models.append((url , model))
        
    def create_model(self, node):
        model = Model(node.attrib['name'])
        model.fields = self.get_fields(node)
        return model

    def get_fields(self, root):
        return [self.create_field(node) for node in root.findall('field')]
    
    def create_field(self, node):
        field_class = eval(node.attrib['parser'])
        field = field_class(node.attrib)
        if field_class == ListField:
            field.model = self.create_model(node.find('model'))
        return field

class Field:

    def __init__(self, attrib):
        self.name = attrib['name']
        self.xpath = attrib['xpath']
        self.type = attrib.get('type', 'str')
            
class SimpleField(Field):
        
    def get_value(self, html):
        value = html.xpath(self.xpath)[0]
        if type(value) != self.type:
            value = self.convert(value)
        return value

    def convert(self, value):
        if self.type == 'str':
            return self.get_str_value(value)
        elif self.type == 'int':
            str_value = self.get_str_value(value)
            return int(str_value)

    def get_str_value(self, value):
        if type(value) == html.HtmlElement:
            text = value.text
            if not text:
                text = self.search_str(value)
            return text
        elif type(value) == lxml.etree._ElementUnicodeResult:
            return str(value)

    def search_str(self, root):
        for node in root.getchildren():
            if node.text:
                return node.text

        for node in root.getchildren():
            text = self.search_str(node)
            if text:
                return text
    
class ListField(Field):
    
    def __init__(self, attrib):
        super().__init__(attrib)
        self.xpath_iter = attrib['xpath_iter']
    
    def get_value(self, tree):
        results = []
        root = tree.xpath(self.xpath)[0]
        
        for node in root.xpath(self.xpath_iter):
            results.append(self.model.get_result(node))
        return results

class Model:
    
    def __init__(self, name):
        self.name = name
        self.fields = []
        
    def get_result(self, root):
        result = type(self.name, (), {})
        for field in self.fields:
            exec('result.{0} = field.get_value(root)'.format(field.name))
        return result

class Parser:
    
    def __init__(self, config):
        self.config = config
        
    def parse(self, url):
        model = self.find_model(url)
        tree = html.fromstring(requests.get(url).text)
        return model.get_result(tree)
    
    def find_model(self, url):
        for page, model in self.config.models:
            if re.match(page, url):
                return model
            
        print('No model found for url : {0}'.format(url))
        exit()
