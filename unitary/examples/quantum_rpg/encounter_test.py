import io
import unitary.examples.quantum_rpg.battle as battle
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.encounter as encounter
import unitary.examples.quantum_rpg.npcs as npcs


def test_trigger():
    e = encounter.Encounter([])
    assert all(e.will_trigger() for _ in range(100))
    e = encounter.Encounter([], 1)
    assert all(e.will_trigger() for _ in range(100))
    e = encounter.Encounter([], 0.0)
    assert all(not e.will_trigger() for _ in range(100))
    e = encounter.Encounter([], 0.5)
    assert not all(e.will_trigger() for _ in range(100))
    assert not all(not e.will_trigger() for _ in range(100))


def test_encounter():
    output = io.StringIO()
    o = npcs.Observer("watcher")
    e = encounter.Encounter([o], output)

    c = classes.Analyst("Aaronson")
    b = e.initiate([c], output)
    b.take_player_turn(user_input=["s", "1", "1"])
    b.take_npc_turn()
    assert (
        output.getvalue().replace("\t", " ").strip()
        == r"""
-----------------------------------------------
Aaronson Analyst   watcher Observer
1QP (0|1> 0|0> 1?)   1QP (0|1> 0|0> 1?)
-----------------------------------------------
Aaronson turn:
s
m
Sample result HealthPoint.HURT
Observer watcher measures Aaronson at qubit Aaronson_1
""".strip()
    )