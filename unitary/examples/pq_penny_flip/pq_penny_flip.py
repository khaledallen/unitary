class GameInterface:
    """
    The user inferface for interacting with the PQ Penny Flip game.
    """
    def __init__(self):
        return

    def play(self):
        print("Welcome to the PQ Penny Flip Game!")

def main():
    game = GameInterface()
    game.play()


if __name__ == "__main__":
    main()