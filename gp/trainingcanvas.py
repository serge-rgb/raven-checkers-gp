class TrainingCanvas(object):
    def __init__(self):
        print 'i am a happy canvas'

    def after(self, time, event):
        if event:
            event()
        else:
            pass  # Do results here

