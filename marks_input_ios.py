# User Settings
title = 'Fluid Loading Q2'
marks = [3, 3, 3, 5, 6]

# Libraries
import sys, mi, ui

# Override some functions
class ExamQuestion(mi.ExamQuestion):
    def __init__(self, title, marks, view):
        super().__init__(title, marks)
        self.view = view

    def __enter__(self):
        return self

    def prompt(self, msg):
        self.view['lblPrompt'].text_color = 'black'
        self.view['lblPrompt'].text = msg

    def disp(self, msg):
        # redefine for gui
        self.view['lblErr'].text_color = 'black'
        self.view['lblErr'].text = msg

    def dispErr(self, msg):
        # redefine for gui
        self.view['lblErr'].text_color = 'red'
        self.view['lblErr'].text = msg

    def getInput(self):
        r = self.view['tfInput'].text
        return r

def refreshState():
    if len(eq.cs) == 0:
        eq.view['cmdEnter'].title = 'Next'
        eq.prompt('🤷🏻 CID:')
        # eq.view['tfInput'].enabled = True
        # eq.view['tfInput'].border_color = '#363636'
    elif len(eq.cs) < len(eq.marks)+1:
        i = len(eq.cs)-1
        mark = eq.marks[i]
        eq.prompt('📜 Part (' + chr(97+i) + ') [' + str(mark) + ' marks]:')
        # eq.view['tfInput'].enabled = True
        # eq.view['tfInput'].border_color = '#363636'
    else:
        eq.prompt('Ready to submit.')
        eq.view['cmdEnter'].title = 'Submit'
        # eq.view['tfInput'].enabled = False
        # eq.view['tfInput'].border_color = '#f6f6f6'
    eq.view['tfInput'].text = ''
    eq.view['tfInput'].begin_editing()

def updateTable(msg):
    eq.view['tvMarks'].text = eq.view['tvMarks'].text + msg + '\n'
    # eq.view['tvMarks'].content_offset = (0, eq.view['tvMarks'].content_size[1] - eq.view['tvMarks'].height)

def action_cmdEnter(sender):
    eq.disp('')
    if len(eq.cs) == 0:
        eq.view['tvMarks'].text = ''
        cid = eq.validateCID(eq.getInput())
        if cid is None:
            return
        else:
            eq.cs = [cid]
            updateTable('CID: ' + '%08d' % cid)
            refreshState()
    elif len(eq.cs) < len(eq.marks)+1:
        i = len(eq.cs)-1
        mark = eq.marks[i]
        score = eq.validateMark(mark, eq.getInput())
        if score is None:
            return
        else:
            eq.cs.append(score)
            updateTable('\t(' + chr(97+i) + ') [' + str(mark) + ' marks]: ' + str(score))
            refreshState()
    else:
        # add a totals column
        eq.cs.append(sum(eq.cs[1:]))
        # screen output
        pc = eq.cs[-1] / sum(eq.marks) * 100
        updateTable('\n----------------------------')
        updateTable('📊 Total mark = '+ str(eq.cs[-1]) + ' (' + '%.0f' % pc + '%)')
        updateTable('----------------------------\n')
        eq.writeRecord()
        i, average_mark, average_pc = eq.cohortAnalytics()
        updateTable(str(i) + ' marked scripts so far.')
        updateTable('Average = ' + '%.0f' % average_mark + ' (' + '%.0f' % average_pc + '%)')
        # updateTable('=========================\n')
        refreshState()
    return

# Build interface
v = ui.load_view('marks_input_ios.pyui')
eq = ExamQuestion(title, marks, v)

v.name = eq.title
v['tfInput'].keyboard_type = ui.KEYBOARD_DECIMAL_PAD
# v['tfInput'].delegate = tfInput_delegate()
v.present('fullscreen')
v['tfInput'].begin_editing()

refreshState()
