class Verifier:
    def __init__(self, data):
        self.data=data

    def check_config(self):
        rtn=True
        if (self.data.host == ""):
            rtn=False
        elif (self.data.username == ""):
            rtn=False
        elif (self.data.password == ""):
            rtn=False
        elif (self.data.database == ""):
            rtn=False
        return rtn

    def check_tables(self):
        # no of fields >0
        # no of primary keys>0
        # field data types
        return True

    def check_data(self):
        rtn=True
        if not self.check_config():
            print("Error in config")
            rtn=False
        if not self.check_tables():
            print("Error in tables")
            rtn=False
        return rtn
