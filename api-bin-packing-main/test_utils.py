import pprint
from Utils import Utils

class DummyTable:
    def __init__(self):
        self.width = 200
        self.height = 100
        self.bin_maxrects = "(0,10,20,30,40,'101'),(0,15,25,30,40,'102'),(0,0,0,50,100,'201')"
        self.bin_skyline    = "(0,5,5,30,40,'101'),(0,0,0,50,100,'201')"
        self.bin_guillotine = "(0,10,10,30,40,'101')"

if __name__ == "__main__":
    table = DummyTable()
    result = Utils.mount_table_return(table)
    print("Resultado de mount_table_return:")
    pprint.pprint(result)
