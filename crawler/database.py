import csv

class Data:
    def __init__(self, filename, datalist):
        self.filename = filename
        self.datalist = datalist
        
    def init_insert(self):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.datalist)
            
            file.close()
        
    def insert(self):
        # To Be Implemented
        return None
    