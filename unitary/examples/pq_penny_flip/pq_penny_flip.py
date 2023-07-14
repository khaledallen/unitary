from unitary.alpha import QuantumObject, QuantumWorld, quantum_if, Flip, Phase
import numpy as np
import enum

class CoinFaces(enum.Enum):
    HEAD = 0
    TAILS = 1

PICARD = 0
Q = 1

class PQPennyFlip:
    def __init__(self):
        self.clear()

    def entangle(self):
        # Build the Bell State via |P>-[H]-*-
        #                                  |
        #                          |Q>-----+-
        Flip(0.5)(self.q_coins[1][PICARD])
        quantum_if(self.q_coins[1][PICARD]).apply(Flip())(self.q_coins[1][Q])
    
    def clear(self):
        coins = []
        coins.append(QuantumObject('picard', CoinFaces.HEAD))
        coins.append(QuantumObject('q', CoinFaces.HEAD))
        self.q_coins = (QuantumWorld(coins), coins)
        self.entangle()

    def measure_and_display(self):
        quantum_if(self.q_coins[1][PICARD]).apply(Flip(0.25))(self.q_coins[1][Q])
        measurement1 = self.q_coins[0].pop([self.q_coins[1][PICARD]])[0]
        measurement2 = self.q_coins[0].pop([self.q_coins[1][Q]])[0]
        print(measurement1, measurement2)


class GameInterface:
    """
    The user inferface for interacting with the PQ Penny Flip game.
    """
    def __init__(self, penny: PQPennyFlip):
        self.penny = penny
        return

    def play(self):
        self.penny.clear()
        print("Welcome to the PQ Penny Flip Game!")
        print("Your goal is to choose a quantum flip that will make sure your coins come up on the same face.")
        phi = float(input("Choose your first gate value: "))
        pi = float(input("Choose your second gate value: "))
        Flip(effect_fraction=phi)(self.penny.q_coins[1][PICARD])
        Phase(effect_fraction=pi)(self.penny.q_coins[1][PICARD])
        rng1 = np.random.default_rng()
        q_phi = rng1.random()
        q_pi = rng1.random()
        print(q_phi, q_pi)
        Flip(effect_fraction=q_phi)(self.penny.q_coins[1][Q])
        Phase(effect_fraction=q_pi)(self.penny.q_coins[1][Q])
        self.penny.entangle()
        self.penny.measure_and_display()

def main():
    pennyFlip = PQPennyFlip()
    game = GameInterface(pennyFlip)
    game.play()



if __name__ == "__main__":
    main()