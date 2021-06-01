from enum import Enum

class Api_type(Enum):
    UNKNOWN = 0
    GET_ONE = 1
    GET_ALL = 2
    UPDATE = 3

class Api:   
    def __init__(self):
        self.api_name=""
        self.table=""
        self.api_type=Api_type.UNKNOWN

    def parse_xml(self, node):
        if node.tag=="api":
            try:
                if node.attrib["type"]=="get_one":
                    self.api_type=Api_type.GET_ONE
                elif node.attrib["type"]=="get_all":
                    self.api_type=Api_type.GET_ALL
                elif node.attrib["type"]=="update":
                    self.api_type=Api_type.UPDATE
                else:
                    self.api_type=Api_type.UNKNOWN
            except:
                self.api_type=Api_type.UNKNOWN
            for child in node:
                if (child.tag=="name"):
                    self.api_name=child.text
                if (child.tag=="table"):
                    self.table=child.text

