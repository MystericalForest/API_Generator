import xml.etree.ElementTree as ET
import file_creater, verifier
import api, table

class Generator_data:
    def __init__(self):
        self.tables=[]
        self.endpoints=[]
        self.host = ""
        self.username = ""
        self.password = ""
        self.database = ""

    def find_table(self, table_name):
        for table in self.tables:
            if table.table_name==table_name:
                return table

class Generator:
    def __init__(self):
        self.data=Generator_data()

    def create_config_file(self):
        config=file_creater.Config_file(self.data.host, self.data.username, self.data.password, self.data.database)
        config.create_config_file()

    def create_sql_tables_file(self):
        sql=file_creater.SQL(self.data.tables)
        sql.create_sql_tables_file()

    def create_CRUD_files(self):
        for table in self.data.tables:
            api=file_creater.CRUD_API_file()
            api.create_CRUD_file(table)

    def create_api_files(self):
        for endpoint in self.data.endpoints:
            api=file_creater.CRUD_API_file()
            api.create_api_file(self.data.find_table(endpoint.table), endpoint)

    def read_tables_from_xml(self, node):
        if node.tag=="tables":
            for child in node:
                tmp=table.Table()
                tmp.parse_xml(child)
                self.data.tables.append(tmp)

    def read_endpoints_from_xml(self, node):
        if node.tag=="endpoints":
            for child in node:
                if child.tag=="api":
                    tmp=api.Api()
                    tmp.parse_xml(child)
                    self.data.endpoints.append(tmp)

    def read_metadata_from_xml(self, node):
        if node.tag=="metadata":
            for child in node:
                if child.tag=="host":
                    self.data.host=child.text
                if child.tag=="username":
                    self.data.username=child.text
                if child.tag=="password":
                    self.data.password=child.text
                if child.tag=="database":
                    self.data.database=child.text

    def generate_all(self):
        verify = verifier.Verifier(self.data)
        if (verify.check_data()):
            self.create_config_file()
            self.create_sql_tables_file()
            self.create_CRUD_files()
            self.create_api_files()
    
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
    generator.generate_all()
