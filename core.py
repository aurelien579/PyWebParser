import re
import requests
from lxml import html

class SimpleFieldParser:
    
    def __init__(self, xpath):
        self.xpath = xpath
    
    def parse(self, tree):
        return tree.xpath(self.xpath)[0]

class Field:

    def __init__(self, name, parser, xpath):
        self.name = name
        self.xpath = xpath
        self.parser = parser(xpath)
        
    def find_value(self, html):
        return self.parser.parse(html)

class Model:
    
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.fields = []

class Parser:
    
    def __init__(self, config):
        self.config = config
        
    def parse(self, url):
        model = self.find_model(url)
        tree = html.fromstring(requests.get(url).text)
        
        result = type(model.name, (), {})
        for field in model.fields:
            exec('result.{0} = {1}'.format(field.name, field.find_value(tree)))
        return result
    
    def find_model(self, url):
        for model in self.config.models:            
            if re.match(model.url, url):
                return model
            
        print('No model found for url : {0}'.format(url))
        exit()