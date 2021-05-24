import xml.etree.ElementTree as ET
import file_creater
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

class Field:   
    def __init__(self):
        self.field_name=""
        self.field_type=""
        self.primary=False

    def is_text_field(self):
        if self.field_type=="varchar":
            return True
        else:
            return False

    def parse_xml(self, node):
        try:
            if node.attrib["primary"]=="yes":
                self.primary=True
        except:
            self.primary=False
        for child in node:
            if (child.tag=="fieldname"):
                self.field_name=child.text
            if (child.tag=="fieldtype"):
                self.field_type=child.text

class Table:    
    def __init__(self):
        self.table_name=""
        self.fields=[]

    def get_non_primary_fields(self):
        rtn=[]
        for field in self.fields:
            if field.primary==False:
                rtn.append(field)
        return rtn

    def get_primary_fields(self):
        rtn=[]
        for field in self.fields:
            if field.primary==True:
                rtn.append(field)
        return rtn

    def parse_xml(self, node):
        for child in node:
            if (child.tag=="tablename"):
                self.table_name=child.text
            if (child.tag=="fields"):
                for field in child:
                   
                    tmp=Field()
                    tmp.parse_xml(field)
                    self.fields.append(tmp)

    def select_text(self):
        sql="SELECT "
        for idx, field in enumerate(self.fields):
            sql+= field.field_name
            if idx<len(self.fields)-1:
                sql+=", "
            else:
                sql+=" "
        sql+="FROM " + self.table_name
        return sql

    def select_one_text(self):
        sql="SELECT "
        for idx, field in enumerate(self.fields):
            sql+= field.field_name
            if idx<len(self.fields)-1:
                sql+=", "
            else:
                sql+=" "
        sql+="FROM " + self.table_name + " WHERE "
        primary=self.get_primary_fields()
        for idx, field in enumerate(primary):
            sql+= field.field_name + " = \". $" + field.field_name
            if idx<len(primary)-1:
                sql+=" . \" AND "
            else:
                sql+=" "
        return sql

    def update_text(self):
        sql="UPDATE " + self.table_name + " SET "
        non_primary=self.get_non_primary_fields()
        primary=self.get_primary_fields()
        for idx, field in enumerate(non_primary):
            sql+= "'" + field.field_name + "'= "
            if field.is_text_field():
                sql+="'"
            sql+= "\". $" + field.field_name
            if field.is_text_field():
                sql+=". \"'"
            if idx<len(non_primary)-1:
                sql+=". \", "
            else:
                sql+=" WHERE "
        for idx, field in enumerate(primary):
            sql+= "'" + field.field_name + "'= \". $" + field.field_name
            if idx<len(primary)-1:
                sql+=". \", "
            else:
                sql+=" "
        return sql

    def print_text(self):
        print("tablename", self.table_name)
        print("fields")
        for field in self.fields:
            print("fieldname", field.field_name, field.field_type)
    
class Generator:
    def __init__(self):
        self.tables=[]
        self.endpoints=[]
        self.host = ""
        self.username = ""
        self.password = ""
        self.database = ""

    def create_config_file(self):
        config=file_creater.Config_file(self.host, self.username, self.password, self.database)
        config.create_config_file()

    def create_sql_tables_file(self):
        sql=file_creater.SQL(self.tables)
        sql.create_sql_tables_file()

    def create_CRUD_files(self):
        for table in self.tables:
            api=file_creater.CRUD_API_file()
            api.create_CRUD_file(table)

    def read_tables_from_xml(self, node):
        if node.tag=="tables":
            for child in node:
                tmp=Table()
                tmp.parse_xml(child)
                self.tables.append(tmp)
                print(tmp.select_one_text())

    def read_endpoints_from_xml(self, node):
        if node.tag=="endpoints":
            for child in node:
                if child.tag=="api":
                    tmp=Api()
                    tmp.parse_xml(child)
                    self.endpoints.append(tmp)

    def read_metadata_from_xml(self, node):
        if node.tag=="metadata":
            for child in node:
                if child.tag=="host":
                    self.host=child.text
                if child.tag=="username":
                    self.username=child.text
                if child.tag=="password":
                    self.password=child.text
                if child.tag=="database":
                    self.database=child.text
    
    def read_xml(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        for child in root:
            if child.tag=="tables":
                self.read_tables_from_xml(child)
            if child.tag=="metadata":
                self.read_metadata_from_xml(child)
            if child.tag=="endpoints":
                self.read_endpoints_from_xml(child)
        

if __name__ == "__main__":
    generator=Generator()
    generator.read_xml("xml\\redapple.xml")
    generator.create_config_file()
    generator.create_sql_tables_file()
    generator.create_CRUD_files()
