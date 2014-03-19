from gamemanager import GameManager


class TrainingContext():
    def __init__(self):
        class ThinkTime:
            def get(self):
                return 0
        self.thinkTime = ThinkTime()
        self.manager = GameManager(root=None, parent=self, training=True)
        self.manager.num_players = 2


def train(ctx):
    'Play a match between a GPController and a alpha beta controller'

if __name__ == '__main__':
    ctx = TrainingContext()
    train(ctx)

