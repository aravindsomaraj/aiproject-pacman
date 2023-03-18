from operator import neg

import kakuro
from kakuro import count, first

class CSP(kakuro.Problem):

    def __init__(self, vars, domains, neighbors, constraints):
        """Construct a CSP problem. If vars is empty, it becomes domains.keys()."""
        super().__init__(())
        vars = vars or list(domains.keys())
        self.vars = vars
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0

    def numconflicts(self, var, val, assignment):
        #to return the number of conflicts encountered

        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])
    
    def assign(self, var, val, assignment):
        
        #to add the variable to the domain list
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        #to unassign the variable from the domain list   
        if var in assignment:
            del assignment[var]

    def actions(self, state):
        #to find and return a list of possible actions
        if len(state) == len(self.vars):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.vars if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.numconflicts(var, val, assignment) == 0]

    def out(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    # These are for constraint propagation

    def support_pruning(self):
        #fn to make sure if the value can be pruned from domain
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.vars}

    def assume(self, var, value):
        #to gain inferences from variable
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        #pruning from domain
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)
# Variable ordering

def first_unassigned_variable(assignment, csp):
    #to go by the variable order
    return first([var for var in csp.vars if var not in assignment])


def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.numconflicts(var, val, assignment) == 0 for val in csp.domains[var])
    
# Value ordering

def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)

# infer

def no_infer(csp, var, value, assignment, removals):
    return True

def forward_checking(csp, var, value, assignment, removals):
    #for pruning neighbour films
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True

#Constraint Propagation with ac3

def dom_up(csp, queue):
    return Sorted(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))

def ac3(csp, queue=None, removals=None, arc_heuristic=dom_up):
    
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.vars for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    cchecks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, cchecks = revise(csp, Xi, Xj, removals, cchecks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, cchecks  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, cchecks  # CSP is satisfiable

def revise(csp, Xi, Xj, removals, cchecks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            cchecks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True
    return revised, cchecks

def mac(csp, var, value, assignment, removals, constraint_propagation=ac3):
    #to maintain arc consistency
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

# backtrking algo

def backtrking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, infer=no_infer):

    def backtrk(assignment):
        if len(assignment) == len(csp.vars):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if csp.numconflicts(var, value, assignment) == 0 :
                csp.assign(var, value, assignment)
                removals = csp.assume(var, value)
                if infer(csp, var, value, assignment, removals):
                    out = backtrk(assignment)
                    if out is not None:
                        return out
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    out = backtrk({})
    return out
