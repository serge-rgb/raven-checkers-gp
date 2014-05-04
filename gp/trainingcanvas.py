class TrainingCanvas(object):
    def __init__(self):
        pass

    def after(self, time, event):
        if event:
            event()
        else:
            pass  # Do results here

