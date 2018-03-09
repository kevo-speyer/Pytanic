def main():
    """ Main Program"""
    # First: Read Data. 
    #Define object person with atributes (Age, Sex, Ticket, etc)

    # Some Data Analysis: Get conditional probabilities ( Prob(surv|fem) , Prob(surv|clas==1), etc
 
def test():
    """Test space to do stuff"""
  
    #Read data. Tripulation is a list with Persons (Class defined below) 
    Tripulation = read_data("train.csv")
    
    B_attr = "status"
    B_value = 1
    
    for attr in "sex", "clas", "port":
        for value in get_attr_opt(attr):
            for B_attr in "sex", "clas", "port":
                for B_value in get_attr_opt(attr):
                    proba = get_cond_proba(Tripulation,attr,value, B_attr,B_value)   
                    print "Probability of "+B_attr+" being "+ str(B_value)+" given that "+ attr + " is ", value, " = ", proba
 
def get_cond_proba(Tripulation, A_field,A_value, B_field, B_value):
    """ Get conditional Probability of A, given B"""
    n_tot = 0
    n_A = 0
    n_B = 0
    n_A_B = 0
    for guy in Tripulation:
        n_tot += 1 
        if(guy.get_attr(A_field) == A_value): # Check B Male
            n_B += 1
             
            if(guy.get_attr(B_field) == B_value): # Check A Survival
                
                n_A_B += 1 

    proba_A_given_B = float(n_A_B) / float(n_B)

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

    return options


if __name__ == "__main__":
    # execute only if run as a script
    test()
