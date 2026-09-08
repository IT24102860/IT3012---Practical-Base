class KnowledgeBase:

    def __init__(self):
        # Store current facts.
        # A set prevents duplicate facts.
        self.facts = set()

        # Store logical rules.
        # Each rule will be:
        # (premises, conclusion)
        self.rules = []

    def tell_fact(self, fact_string):
        # Add a new fact to the knowledge base.
        self.facts.add(fact_string)

    def tell_rule(self, premise_list, conclusion_string):
        # Add a new rule to the knowledge base.
        self.rules.append(
            (premise_list, conclusion_string)
        )

    def clear_facts(self):
        # Remove all current facts.
        # Rules are NOT deleted.
        self.facts.clear()

    def forward_chain(self):

        # Start the reasoning process.
        new_facts_added = True

        # Continue while new knowledge is being produced.
        while new_facts_added:

            # Assume nothing new will be found in this pass.
            new_facts_added = False

            # Check every rule.
            for premises, conclusion in self.rules:

                # No need to derive something
                # that is already known.
                if conclusion not in self.facts:

                    # Check whether ALL premises
                    # are currently facts.
                    if all(
                        premise in self.facts
                        for premise in premises
                    ):

                        # Derive the conclusion.
                        self.facts.add(conclusion)

                        # New knowledge was generated,
                        # so another pass is required.
                        new_facts_added = True