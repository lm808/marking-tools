# User Settings
title = 'Fluid Loading Q2'
marks = [3, 3, 3, 5, 6]

# Commandline version
from mi import ExamQuestion
import sys

eq = ExamQuestion(title, marks)
print('\n' + title + '\n=========================')

while True:
    try:
        # get CID and make sure it is valid
        msg = '\nCID: '
        cid = eq.validateCID(eq.getInput(msg))
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
        print('-------------------------')
        print('Total mark =', eq.cs[-1], '(' + '%.0f' % pc + '%)')
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