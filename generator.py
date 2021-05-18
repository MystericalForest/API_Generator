import xml.etree.ElementTree as ET
import create_sql

class Field:
    
    def __init__(self):
        self.field_name=""
        self.field_type=""

    def parse_xml(self, node):
        for child in node:
            if (child.tag=="fieldname"):
                self.field_name=child.text
            if (child.tag=="fieldtype"):
                self.field_type=child.text   

class Table:    
    def __init__(self):
        self.table_name=""
        self.fields=[]

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

    def print_text(self):
        print("tablename", self.table_name)
        print("fields")
        for field in self.fields:
            print("fieldname", field.field_name, field.field_type)
    

def read_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:
        tmp=Table()
        tmp.parse_xml(child)
        print(tmp.select_text())
        sql=create_sql.SQL(tmp)
        sql.get_create_table_file()

if __name__ == "__main__":
   read_xml("xml\\redapple.xml")
