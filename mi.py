import csv, re, readline
from math import floor

class ExamQuestion:
    # property default values
    # none required.

    def __init__(self, title, marks):
        self.title = title
        self.marks = marks
        self.fn = title.replace(' ', '_') + '.csv'
        self.cs = []
    
    def __enter__(self):
        return self
    
    def disp(self, msg):
        # redefine for gui
        print(msg)

    def dispErr(self, msg):
        # redefine for gui
        print(msg)
    
    def getInput(self, msg):
        # redefine for gui
        r = input(msg)
        return r
    
    def cohortAnalytics(self):
        with open(self.fn, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            average_mark = 0
            for i, line in enumerate(reader, start=1):
                # convert strings read from csv back to integers
                line = [int(x) for x in line]
                average_mark = average_mark + line[-1]
            average_mark = average_mark/i
            pc = average_mark / sum(self.marks) * 100
            return i, average_mark, pc
    
    def chkDupes(self, cid):
        cid = cid.lstrip('0')
        if cid == '':
            cid = '0'
        try:
            with open(self.fn, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for line in reader:
                    if cid==line[0]:
                        return True
                return False
        except FileNotFoundError:
            self.disp('No CSV file yet.')
            return False
    
    def writeRecord(self):
        with open(self.fn, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(self.cs)
        self.cs = []

    def chkStrInput(self, r):
        # allow exit
        if r.lower()=='q' or r.lower()=='exit' or r.lower()=='...':
            raise KeyboardInterrupt
        if r.lower()=='back':
            return r.lower()
        # remove all non-numeric values
        r = re.sub("[^0-9]", "", r)
        # empty?
        if len(r)==0:
            self.dispErr('No numeric values in input.')
            return None
        # ensure you can convert it to a number
        try:
            float(r)
            return r
        except:
            self.dispErr('Numeric input only.')
            return None
        
    def validateCID(self, r):
        if self.chkStrInput(r) is None:
            return None
        else:
            r = self.chkStrInput(r)
        if len(r) != 8:
            self.dispErr(r + ' is not a valid CID.')
            return None
        if self.chkDupes(r):
            self.dispErr('Duplicate CID found.')
            return None
        return int(r)

    def validateMark(self, mark, r):
        if self.chkStrInput(r) is None:
            return None
        else:
            r = self.chkStrInput(r)
        def mathsRound(r):
            return int(floor(float(r)+0.5))
        if mathsRound(r)>mark or mathsRound(r)<0:
            self.dispErr('Invalid mark.')
            return None
        return mathsRound(r)
