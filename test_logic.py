from logic_engine import KnowledgeBase


def test_forward_chaining():

    # Create an empty Knowledge Base
    kb = KnowledgeBase()

    # -----------------------------------------
    # ADD THE TWO DOMAIN RULES
    # -----------------------------------------

    # Rule 1:
    # TargetVisible AND HasDust
    # -> SafeToEngage
    kb.tell_rule(
        ["TargetVisible", "HasDust"],
        "SafeToEngage"
    )

    # Rule 2:
    # SafeToEngage AND BloodseekerMissing
    # -> Retreat
    kb.tell_rule(
        ["SafeToEngage", "BloodseekerMissing"],
        "Retreat"
    )


    # =========================================
    # TEST CASE 1
    # =========================================

    kb.clear_facts()

    kb.tell_fact("TargetVisible")
    kb.tell_fact("HasDust")

    kb.forward_chain()

    assert "SafeToEngage" in kb.facts
    assert "Retreat" not in kb.facts

    print("Test 1 Passed")
    print("Facts:", kb.facts)


    # =========================================
    # TEST CASE 2
    # =========================================

    kb.clear_facts()

    kb.tell_fact("TargetVisible")
    kb.tell_fact("HasDust")
    kb.tell_fact("BloodseekerMissing")

    kb.forward_chain()

    assert "Retreat" in kb.facts

    print("Test 2 Passed")
    print("Facts:", kb.facts)

    print("All Logic Engine Test Cases Passed!")


if __name__ == "__main__":
    test_forward_chaining()