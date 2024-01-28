# User Settings
title = 'Question Title'
marks = [3, 3, 3, 5, 6]
class_list = None
flip_list = False

# Commandline version
from mi import ExamQuestion
import sys, readline

print('\n' + title + '\n=========================')

eq = ExamQuestion(title, marks, class_list, flip_list)

while True:
    try:
        # get CID and make sure it is valid
        if eq.cl is not None:
            dCID = eq.getDefaultCID();
            msg = '\nCID (ENTER for default = ' + dCID + '): '
            cid = eq.getInput(msg)
            if cid == '':
                cid = dCID
        else:
            msg = '\nCID: '
            cid = eq.getInput(msg)
        cid = eq.validateCID(cid)
        while cid is None:
            cid = eq.validateCID(eq.getInput(msg))
        eq.cs = [cid]
        # get score for each part and make sure it is valid
        for i, mark in enumerate(eq.marks, start=0):
            msg = 'Part (' + chr(97+i) + ') [' + str(mark) + ' marks]: '
            score = eq.validateMark(mark, eq.getInput(msg))
            while score is None:
                score = eq.validateMark(mark, eq.getInput(msg))
            eq.cs.append(score)
        # add a totals column
        eq.cs.append(sum(eq.cs[1:]))
        # screen output
        pc = eq.cs[-1] / sum(eq.marks) * 100
        CRED = '\033[91m'
        CEND = '\033[0m'
        print('-------------------------')
        print('Total mark =', CRED, eq.cs[-1], CEND, '(' + '%.0f' % pc + '%)')
        print('-------------------------')
        eq.writeRecord()
        i, average_mark, average_pc = eq.cohortAnalytics()
        print(i, 'marked scripts so far.')
        print('Average =', '%.0f' % average_mark, '(' + '%.0f' % average_pc + '%)')
        print('=========================')      
    except KeyboardInterrupt:
        print('\nQuit.\n')
        sys.exit(0)
    except:
        raise
