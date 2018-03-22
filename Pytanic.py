attr_list = ["sex", "clas", "port", "age_group", "siblings_group","parents_group"]
label = "status" 
def main():
    """ Descision Tree Main Program"""
    # 1) Configuration: Set attributes, label
    # 2) First: Read Data
    #Tripulation = read_data("train.csv")
    # 3) Train Model
    # 4) Predict

def test():
    """Test space to do stuff"""
  
    #Read data. Tripulation is a list with Persons (Class defined below) 
    tripulation = read_data("train.csv")
    
    #Train model
    n_data = len(tripulation) # Set a global variable
    # Build tree
    tree = build_tree(tripulation, n_data) # Train data

    #for branch in tree:
        #print "branch.ques,branch.answ,branch.pos, branch.t_br, branch.f_br"
        #print branch.ques,branch.answ,branch.pos, branch.t_br, branch.f_br

    #Predict on test set
    #test_set = read_test_set("test.csv")
    n_corr = 0
    for guy in tripulation :
        prediction = predict_single(guy,tree)
        if int(2*(1.-prediction)) == guy.get_attr("status") :
            n_corr += 1

    print "Correctly predicted precetage of deaths:", float(n_corr) / float(n_data)

    
def predict_single(person, tree):
    """ use the decision tree to predict the status of one person"""
    
    ques = 1
    node = 0
    while ques != 0:
        for branch in tree:
            #print branch.pos,node
            if branch.pos == node:
                ques = branch.ques
                if person.get_attr(branch.ques) == branch.answ :
                    node = branch.t_br
                else :
                    node = branch.f_br
                break
        death_proba = branch.death_proba
    return death_proba
       

def build_tree(data, init_pop, node_num = 0,tree = []):
    """ Build a Descicion tree """
 
    # Check if this node ends here or has ramifications
    end_branch = check_end_branch(data, init_pop)

    death_proba = get_proba(data, "status", 0)
    if end_branch == True :
        # If it ends here, save probability of dead for this leaf
        #death_proba = get_proba(data, "status", 0)
        true_node_num = 0 # Set the branches to 0 indicates that the Node is terminal
        false_node_num = 0 # and it has no new branches
        best_ques = 0
        best_answ = 0 
    else:  # If it does not end here, then
        # get best question and answer
        best_ques, best_answ = get_best_split(data) 
        if best_ques == 0: 
            #death_proba = get_proba(data, "status", 0)
            true_node_num = 0 # Set the branches to 0 indicates that the Node is terminal
            false_node_num = 0 # and it has no new branches
            best_ques = 0
            best_answ = 0 
            end_branch = True
        else:      
            # Slice data in two groups: 
            # 1) best_ques == best_anse => True_data
            # 2) best_quest != best_answ => False_data
            true_data, false_data = split_data(data, best_ques, best_answ)
                
        #give each new node an ID
        last_node = len(tree)
        true_node_num = last_node + 1
        false_node_num = last_node + 2
  
    #DEBUG
    #print "best_ques, best_answ, node_num, true_node_num, false_node_num"
    #print best_ques, best_answ, node_num, true_node_num, false_node_num
    #/DEBUG
 
    new_node = Node(best_ques, best_answ, node_num, true_node_num, false_node_num, death_proba)

    if end_branch == True :
        #print "BRANCH ENDED, DEATH PROBA:"
        new_node.death_proba = death_proba    
        #print new_node.death_proba
    
    tree.append(new_node)

    if end_branch == False:
        # Recursively Generate new nodes in the tree
        tree = build_tree(true_data, init_pop, true_node_num, tree)
        tree = build_tree(false_data, init_pop, false_node_num, tree)

    return tree

class Node:
    """ This is a branch a of tree. A tree is build of Nodes """
    def __init__(self,ques, answ, pos, true_branch, false_branch, d_prb): 
        self.ques = ques
        self.answ = answ 
        self.pos = pos # position on the tree list of Nodes
        self.t_br = true_branch
        self.f_br = false_branch
        self.death_proba = d_prb


def split_data(data, ques, answ):
    """This routine splits the data, given a question and an answer"""
    true_data = []
    false_data = []
    for instance in data:
        if instance.get_attr(ques) == answ :
            true_data.append(instance)
        else :  
            false_data.append(instance) 

    return true_data, false_data  
 
def get_best_split(data):
    """ Get the attribute and attribute option to split in the best possible way the data into two groups"""
    best_gini_split = 0.
    best_ques = 0
    best_answ = 0
    init_gini = get_gini(data) 
    for B_attr in attr_list:
        for B_value in get_attr_opt(B_attr):
            p_t = get_proba(data, B_attr, B_value) 
            p_f = 1. - p_t           

            gini_true =  get_cond_proba(data,"status",0, B_attr,B_value)  
            gini_true = 2. * gini_true * ( 1. - gini_true )
            
            gini_false =  get_cond_proba_false(data,"status",0, B_attr,B_value)
            gini_false = 2. * gini_false * ( 1. - gini_false )

            gini_split = init_gini - p_t * gini_true - p_f * gini_false
            if gini_split > best_gini_split :
                best_gini_split = gini_split
                best_ques = B_attr
                best_answ = B_value
    
    
    return best_ques, best_answ

def get_gini(data):
    """ Gets the Gini coefficient of a population"""
    proba = get_proba(data, "status", 0)
    gini_coef = 2.*proba*(1.-proba)
    return gini_coef

def check_end_branch(data, init_pop):
    """ This is the criterion to determine if the branch ends here (leaf) or not"""

    current_population = len(data) 
    pop_fract =  float(current_population) / float(init_pop)
    
    if pop_fract < 0.1 : #If branch has less than 0.1 of the total population, end leaf
        rta = True
    else:
        rta = False

    return rta

def train(data,q_ls=[],a_ls=[],forb_attr=0):
    """ Train with data set"""
    import copy 

    if len(data) < 20:
        return q_ls, a_ls

    data_local = copy.copy(data) 
    attr = label    
    value = 0

    prior_proba = get_proba(data_local, attr, value)    
  
    best_new_info = 0. 
    
    for B_attr in attr_list:
        if B_attr == forb_attr :
            continue
        for B_value in get_attr_opt(B_attr):            
            new_info = ( get_cond_proba(data_local,attr,value, B_attr,B_value) - prior_proba) **2         
            #print "Probability of "+attr+" being "+ str(value)+" given that "+ B_attr + " is ", B_value, " = ", proba
 
            if new_info > best_new_info :
                best_new_info = new_info 
                best_ques = B_attr
                best_answ = B_value
                      
    #print "best question ", best_ques
    #print "best answer " , best_answ           
    #print "best new info" , best_new_info

    q_ls.append(best_ques)
    a_ls.append(best_answ)

    # Generate 2 lists, dividing wether the attribute "best_ques" is best_answ or not
    data_1 = []
    data_2 = []
    for instance in data:
        if instance.get_attr(best_ques) == best_answ :
            data_1.append(instance)
        else : 
            data_2.append(instance)

    #print "len(data_1)" , len(data_1)
    #print "len(data_2)" , len(data_2)

    train(data_1,q_ls,a_ls,best_ques)


def get_proba(data, field, value):
    """ Estimate probability from data of field being == value """

    n_tot = 0
    n_A = 0

    for guy in data:
        n_tot += 1
        if(guy.get_attr(field) == value): # Check A
            n_A += 1

    if n_tot > 0:
        proba = float(n_A) / float(n_tot)
    else:
        proba = 0.

    return proba

def get_cond_proba(Tripulation, A_field,A_value, B_field, B_value):
    """ Get conditional Probability of A, given B"""
    n_tot = 0
    n_A = 0
    n_B = 0
    n_A_B = 0
    for guy in Tripulation:
        n_tot += 1 
        if(guy.get_attr(B_field) == B_value): # Check B 
            n_B += 1
             
            if(guy.get_attr(A_field) == A_value): # Check A 
                
                n_A_B += 1 
    
    if n_B > 0:
        proba_A_given_B = float(n_A_B) / float(n_B)
    else:
        proba_A_given_B = 0.

    return proba_A_given_B

def get_cond_proba_false(Tripulation, A_field,A_value, B_field, B_value):
    """ Get conditional Probability of A, given (not B)"""
    n_tot = 0
    n_A = 0
    n_B = 0
    n_A_B = 0
    for guy in Tripulation:
        n_tot += 1 
        if(guy.get_attr(B_field) != B_value): # Check B 
            n_B += 1
             
            if(guy.get_attr(A_field) == A_value): # Check A 
                
                n_A_B += 1 
    
    if n_B > 0:
        proba_A_given_B = float(n_A_B) / float(n_B)
    else:
        proba_A_given_B = 0.

    return proba_A_given_B




def read_data(in_file):
    """Read data from input file, and Create and fill list of Persons
    Return the filled list Tripulation, with data"""
    
    Tripulation = []
    n_line = 0

    with open(in_file, 'r') as f:

        for line in f: # loop over lines (persons)
            n_line += 1

            line = line.rstrip('\n') # Don't tead end of file as string

            if (n_line <= 1 ): # Skip the first line (Headers)
                continue

            new_line = line.split(",")
            PassengerId = int(new_line[0])
            Survived = int(new_line[1])
            Pclass = int(new_line[2])
            Name = str(new_line[3] + new_line[4])
            if(new_line[5]=="male"):    
                Sex = 0
            elif (new_line[5]=="female"):
                Sex = 1
            if (new_line[6]==""):
                Age = "NaN"
            else:
                Age = float(new_line[6])
            SibSp = int(new_line[7])
            Parch = int(new_line[8])
            Ticket = str(new_line[9])
            Fare = float(new_line[10])
            Cabin = str(new_line[11])
            #print new_line[12]
            Embarked = str(new_line[12])
            if "Q" in Embarked:
                Embarked = "Q"
            elif "C" in Embarked:
                Embarked = "C"
            elif "S" in Embarked:
                Embarked = "S"

            new_Person = Person(PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked)
          
            Tripulation.append(new_Person)

    return Tripulation
  
class Person:
    """Each person has attributes"""
    def __init__(self, PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked):
        self.num = PassengerId
        self.status = Survived # 0 = dead; 1 = alive
        self.clas = Pclass # 1 = First Class; 2 = Second Class; 3 = Third Class
        self.name = Name 
        self.sex = Sex # 0 is male # 1 is female
        self.age = Age
        self.siblings = SibSp # Number of Siblings or Spouses
        self.parents = Parch # Number of Parents or Children
        self.ticket = Ticket # Ticket Number
        self.fare = Fare # Cost of the ticket
        self.cabin = Cabin # Cabin Number
        self.port = Embarked # C = Cherbourg, Q = Queenstown, S = Southampton
 
        # Set categories for age. Bound variables to have discrete attributes
        if self.age < 5 : 
            self.age_group = "A"
        elif self.age > 5 and self.age < 12 : 
            self.age_group = "B"
        elif self.age > 12 and self.age < 18 : 
            self.age_group = "C"
        elif self.age > 18 and self.age < 60 :
            self.age_group = "D"
        elif self.age > 60 :
            self.age_group = "E"
        else :
            self.age_group = "NaN"

        # Set categories for parents. Bound variables to have discrete attributes
        if self.parents == 0 :
            self.parents_group = "A"
        elif self.parents == 1 : 
            self.parents_group = "B"
        elif self.parents == 2 : 
            self.parents_group = "C"
        elif self.parents > 2 : 
            self.parents_group = "D"

        # Set categories for siblings. Bound variables to have discrete attributes
        if self.siblings == 0 :
            self.siblings_group = "A"
        elif self.siblings == 1 : 
            self.siblings_group = "B"
        elif self.siblings == 2 : 
            self.siblings_group = "C"
        elif self.siblings > 2 : 
            self.siblings_group = "D"

    def get_attr(self,name_of_attr):
        """ Define a method thar returns the desired attribute name_of_attr, passed as a string""" 
        for attri, value in self.__dict__.iteritems():
            if(attri == name_of_attr):
                return value
   

def get_attr_opt(name_of_attr):
    options = []
    if (name_of_attr == "status"):    
        options = [0, 1]
    if (name_of_attr == "clas"):
        options = [1, 2, 3]
    if (name_of_attr == "sex"):
        options = [0,1]
    if (name_of_attr == "port"):
        options = ["Q","S","C"]
    if (name_of_attr == "siblings"):
        options = ["A","B","C"]
    if (name_of_attr == "parents"):
        options = ["A","B","C"]
    if (name_of_attr == "age_group"):
        options = ["A","B","C","D","E","NaN"]
    if (name_of_attr == "siblings_group"):
        options = ["A","B","C","D"]
    if (name_of_attr == "parents_group"):
        options = ["A","B","C","D"]
    return options


if __name__ == "__main__":
    # execute only if run as a script
    test()
