from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy


class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 

        # TODO: implement backtracking search. 

        # Note that the display and test functions in the main file take domains as inputs. 
        #   So when returning the final solution, make sure to take your assignment function 
        #   and turn the value into a single element list and return them as a domain map. 
        # (0,0) -> (0,8) first row
        # (1,0) -> (1,8) second row etc
        delta = []
        assignment = {}
        assignment["Conflict"] = 0
        while True:
            # display(domains)
            # print()
            assignment, domains = self.Propagate(assignment,domains)

            if assignment["Conflict"] == 1:
                if len(delta) == 0:
                    return "No Solution"
                else:
                    assignment,domains = self.BackTrack(delta)
            else:
                if len(assignment) >= 81:
                    return domains
                else:
                    assignment, x = self.MakeDecision(assignment,domains)
                    # print("decision ",x, " ", assignment[x])
                    delta.append([copy.deepcopy(assignment),x, copy.deepcopy(domains)])
                    domains[x] = [assignment[x]]

        return domains

    # TODO: add any supporting function you need
    def Propagate(self, assignment, D):
        domain_key = D.keys()
        N_s = [0,1,2,3,4,5,6,7,8]
        assignment["Conflict"] = 0
        while True:
            for key in domain_key:
                if len(D[key]) == 1 and key not in assignment.keys():
                    assignment[key]=D[key][0]
            for a in assignment.keys():
                if(a != "Conflict"):
                    D[a] = [assignment[a]]
            for key in domain_key:
                if len(D[key]) == 0:
                    assignment["Conflict"] = 1
                    return assignment, D
            #If does not meet the constraint
            #Check Row
            #Check Column
            #Check Box
            check = True
            for key in domain_key:
                for n in N_s:
                    if (key[0],n) != key and len(D[(key[0],n)]) == 1:
                        if D[(key[0],n)][0] in D[key]:
                            D[key].remove(D[(key[0],n)][0])
                            check = False
                for n in N_s:
                    if (n,key[1]) != key and len(D[(n,key[1])]) == 1:
                        if D[(n,key[1])][0] in D[key]:
                            D[key].remove(D[(n,key[1])][0])
                            check = False
                i = int(key[0]/3)
                j = int(key[1]/3)
                for x in range(3):
                    for y in range(3):
                        if( (i*3)+x , (j*3)+y ) != key and len(D[( (i*3)+x , (j*3)+y ) ]) == 1:
                            if D[( (i*3)+x , (j*3)+y ) ][0] in D[key]:
                                D[key].remove(D[( (i*3)+x , (j*3)+y ) ][0])
                                check = False
            if check:
                return assignment, D
        return assignment, D

    def MakeDecision(self, assignment, D):
        keys = D.keys()
        a = assignment.keys()
        min_choices = 9
        choice_key = 0
        for key in keys:
            if len(D[key]) < min_choices and key not in a and len(D[key]) > 1:
                min_choices = len(D[key])
                choice_key = key

        assignment[choice_key] = random.choice(D[choice_key])
        return assignment, choice_key

    def BackTrack(self, delta):
        assignment, x, D = delta.pop(len(delta)-1)
        assigned = assignment.pop(x)
        D[x].remove(assigned)
        return assignment, D


sd_domain = list(range(0, SD_SIZE))

def check_draw_delim(ind):
    return ((ind + 1) != SD_SIZE) and ((ind + 1) % SD_DIM == 0)

def display(domains):
    for i in sd_domain:
        for j in sd_domain:
            d = domains[(i,j)]
            if len(d) == 1:
                print(d[0], end='')
            else: 
                print('.', end='')
            if check_draw_delim(j):
                print(" | ", end='')
        print()
        if check_draw_delim(i):
            print("-" * (SD_DIM * SD_DIM + 3 * (SD_DIM - 1)))
















    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
