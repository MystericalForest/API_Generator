import xml.etree.ElementTree as ET
import api

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
