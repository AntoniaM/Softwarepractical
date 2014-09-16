# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 17:18:50 2014

@author: Antonia
"""
from __future__ import division
from  scipy       import *
from  matplotlib.pyplot import *


class Tracenode(object):  
    '''
    An instance of the class represents a node in a computational graph for a function.
    '''
    it = 0 # serves as counter for the instances created..
    #Tracenodelist = []  #in this list, all the created instances will be stored
    storelist = [] #the storelist will be used when setting the attribute 'active' of active Tracenode instances to 'True'
        
    def __init__(self, x):
        '''
        An object of the class Tracenode is initialized with a float or integer, 
        the actual value of the node which is created.
        Attributes:
        -self.x:            actual value of the node
        -self.i:            id-number of the node
        -self.origin:       set containing the input nodes which flow into the computation of the node self
        -self.contributesto:set containing the result nodes, in whose comoputation the node self flows into
        -self.parents:      list containing the nodes the created node is computed out of
        -self.children:     list containing the nodes for whose computation the node self is needed for
        -self.operation:    states the operation self.x arises out of     
        -self.opconst:      states if the operation was performed using a constant (when self.parents is a list of length 1)
        -self.depth:        gives the depth of the node in the Graph
        -self.visited:      when the node is in a graph, the attribute visited can be used to memorize, if this node has already been visited
        '''
        if not isinstance(x, float):
            if isinstance(x,int):
                x = float(x)
            else:
                raise TypeError('input argument of function needs to be a float.')
        self.x = x 
        self.i = Tracenode.it
        self.parents = [self] #if the created Tracenode is a result of an operation, then self.parents will be set to the corresponding parents ids while the operation is executed..
        self.children = []
        self.origin = set([self])
        self.contributesto = set()
        self.operation = 'Id' #Default value: Identity function        
        self.opconst = None #states, if the operation was performed using a constant
        self.visited = False
        self.depth = 0
        Tracenode.it = Tracenode.it+1
        #Tracenode.Tracenodelist.append(self) #stores all the during a function evaluation created objects of type Tracenode in a list.
        

    def __repr__(self):
        # for reasons of readability, instead of printing the set origin, a list of the tracer numbers of the Tracenodes contained in the set origin is printed..
        ortrace = []
        for x in self.origin:
            ortrace.append(x.i)
        # for reasons of readability, instead of printing the list of Tracenodes in parents, a list of the tracer numbers of the Tracenodes contained in the list parents is printed.
        contrtrace = []
        for x in self.contributesto:
            contrtrace.append(x.i)
        parentstrace  = []
        for x in self.parents:
            parentstrace.append(x.i)
        # for reasons of readability, instead of printing the list of Tracenodes in children, a list of the tracer numbers of the Tracenodes contained in the list children is printed.
        childrentrace = []
        for x in self.children:
            childrentrace.append(x.i)
        return ' tracer no. {} \tdepth: {}\tparents: {} \toperation: {}\twith const.: {}\tchildren: {}\torigin: {}\tcontributesto: {}\tvalue {}\n'.format(self.i, self.depth, parentstrace, self.operation,self.opconst, childrentrace, ortrace ,contrtrace, self.x)
        
        
    def __add__(self, other):
        '''
        method __add__:     overloads the add operator, so it can be used for data of type Tracenode. 
                            works for the addition of data of type Tracenodes, 
                            Tracenode and integer, Tracenode and float. and vice versa.
        -input:     Tracenode, Tracenode/integer/float
        -output:    Tracenode addit, where addit.x contains the value of the addition, 
                    addit.origin contains a list of the tracenumbers of the summands,
                    addit.operation states, that addit was created by an addition
        '''
        if not isinstance(other, Tracenode):        #for v+2 e.g., we first look, if there already was a node created for this 2 or if we have to create a new one...            
            if isinstance(other, int):
                other = float(other)
            else: 
                if not isinstance(other,float):
                    raise TypeError('Addition is only defined for types Tracenode and Tracenode or float or int.')
            addit = Tracenode(self.x + other)     
            addit.opconst = other 
            addit.parents = [self] 
            addit.origin = self.origin
            addit.depth = self.depth + 1
        else:
            addit = Tracenode(self.x + other.x)          
            addit.parents = [self, other]
            other.children.append(addit)
            addit.origin = self.origin | other.origin
            addit.depth = max(self.depth,other.depth) +1
        self.children.append(addit)
        addit.operation = 'add'
        #print(addit)
        return addit


        
    def __radd__(self,other):
        return self+other
    
    
    def __sub__(self, other):
        '''
        method __sub__:     overloads the sub operator, so it can be used for data of type Tracenode.
                            works for the subtraction of data of type Tracenodes,
                            Tracenode and integer, Tracenode and float. and vice versa.
        -input:     Tracenode, Tracenode/integer/float
        -output:    Tracenode subtr, where subtr.x contains the value of the subtraction,
                    subtr.origin contains a list of the tracenumbers of the summands
        '''
        if not isinstance(other, Tracenode):        #for v+2 e.g., we first look, if there already was a node created for this 2 or if we have to create a new one...            
            if isinstance(other, int):
                other = float(other)
            else:
                if not isinstance(other,float): 
                    raise TypeError('Subtraction is only defined for types Tracenode and Tracenode or float or int.')
            subtr = Tracenode(self.x - other)     
            subtr.opconst = other
            subtr.parents = [self]   
            subtr.origin = self.origin
            subtr.depth = self.depth + 1
        else:
            subtr = Tracenode(self.x - other.x)     
            subtr.parents = [self, other]
            other.children.append(subtr.i)
            subtr.origin = self.origin | other.origin
            subtr.depth = max(self.depth,other.depth) +1
        self.children.append(subtr)
        subtr.operation = 'sub' 
        #print(subtr)
        return subtr
    
    def __rsub__(self,other=0.):
        return self-other
        
    def __neg__(self):
        nega = Tracenode(-self.x)
        nega.parents = [self]
        nega.origin = self.origin
        nega.depth = self.depth +1
        self.children.append(nega)
        nega.operation = 'neg'
        return nega        
        
            
    def __mul__(self, other):
        '''method __mul__:  overloads the mul operator, so it can be used for data of type Tracenode.
                            works for the multiplication of data of type Tracenodes,
                            Tracenode and integer, Tracenode and float. and vice versa.
        -input:     Tracenode, Tracenode/integer/float
        -output:    Tracenode multip, where multip.x contains the resultvalue of the multiplication,
                    multip.origin contains a list of the tracenumbers of the factors.
        '''
        if not isinstance(other, Tracenode):        #for v+2 e.g., we first look, if there already was a node created for this 2 or if we have to create a new one...            
            if isinstance(other, int):
                other = float(other)
            else: 
                if not isinstance(other,float):
                    raise TypeError('Multiplication is only defined for types Tracenode and Tracenode or float or int.')
            multip = Tracenode(self.x * other)     
            multip.opconst = other
            multip.parents = [self] 
            multip.origin = self.origin
            multip.depth = self.depth +1
        else:
            multip = Tracenode(self.x * other.x)
            multip.parents = [self, other]
            other.children.append(multip)        
            multip.origin = self.origin | other.origin
            multip.depth = max(self.depth,other.depth) +1
        self.children.append(multip)
        multip.operation = 'mul'  
        #print(multip)
        return multip
        
        
    def __rmul__(self,other):
        return self*other
        
        
    def __div__(self,other):
        '''method __div__:  overloads the div operator, so it can be used for data of type Tracenode.
                            works for the division of data of type Tracenodes,
                            Tracenode and integer, Tracenode and float. and vice versa.
        -input:     Tracenode, Tracenode/integer/float
        -output:    Tracenode divis, where divis.x contains the resultvalue of the division,
                    divis.origin contains a list of the tracenumbers of the factors.
        '''
        if not isinstance(other, Tracenode):        #for v+2 e.g., we first look, if there already was a node created for this 2 or if we have to create a new one...               
            if other ==0:
                raise ZeroDivisionError('Division by Zero not possible')
            if isinstance(other, int):
                other = float(other)
            else:
                if not isinstance(other,float): 
                    raise TypeError('Division is only defined for types Tracenode and Tracenode or float or int.')
            divis = Tracenode(self.x / other)     
            divis.opconst = other
            divis.parents = [self]  
            divis.origin = self.origin
            divis.depth = self.depth + 1
        else:
            divis = Tracenode(self.x / other.x)       
            divis.parents = [self, other]
            other.children.append(divis)
            divis.origin = self.origin | other.origin
            divis.depth = max(self.depth,other.depth) +1
        self.children.append(divis)
        divis.operation = 'div'
        #print(divis)
        return divis
        
        
    def __pow__(self, other):
        '''
        method __pow__: overloads the pow operator, so it can be used for data of type Tracenode.
                        data of type Tracenodes can be taken to the power of data of type integers.
        -input:     Tracenode, integer
        -output:    Tracenode power, where power.x contains the value of the Tracenodevalue to the power of the integer,
                    power.origin contains a list (with only one element) of the tracenumber of the Tracenode, 
                    which is taken to the power of the integer..
        '''
        if not isinstance(other, int):
            raise TypeError('function power is only defined for to the power of integers.')
        power = Tracenode(self.x**other)
        power.parents = [self]
        power.operation = 'pow'
        self.children.append(power)
        power.opconst = other
        power.origin = self.origin
        power.depth = self.depth +1
        #print(power)
        return power
        
        
    def sin(self):
        '''
        method __sin__: overloaded the sin operator, so it can be used for data of type Tracenode.
        -input:     Tracenode self
        -outbput:   Tracendoe(sin(self.x))
        '''
        sinu = Tracenode(sin(self.x))
        sinu.operation = 'sin'
        self.children.append(sinu)
        sinu.parents = [self]
        sinu.origin = self.origin
        sinu.depth = self.depth +1
        #print(sinu)
        return sinu
        
    def cos(self):
        '''method __cos__: overloaded the cos operator, so it can be used for data of type Tracenode.
        -input:     Tracenode self
        -output:    Tracenode(cos(self.x))
        '''
        cosi = Tracenode(cos(self.x))
        cosi.operation = 'cos'
        self.children.append(cosi)
        cosi.parents = [self]
        cosi.origin = self.origin
        cosi.depth = self.depth +1
        #print(cosi)
        return cosi
        
        
    def exp(self):
        '''method __exp__: overloaded the exp operator, so it can be used for data of type Tracenode.
        -input:     Tracenode self
        -output:    Tracenode(exp(self.x))
        '''
        expo = Tracenode(exp(self.x))
        expo.operation = 'exp'
        self.children.append(expo)
        expo.origin = self.origin
        expo.parents = [self]
        expo.depth = self.depth +1
        #print(expo) 
        return expo
        
    
    def __eq__(self, other):
        '''
        method __eq__:  overloads the eq operator, so it can be used to compare data with data of
                        type Tracenode. If it compares two Tracenodes, it checks if they have the same
                        tracer number(.i) and value(.x).
        -input:     Tracenode, other 
        -output:    returns True, if it compared Tracenodes and they had the same id and value, 
                    returns False in any other case.
        '''
        eq = False
        if isinstance(other,Tracenode):
            if self.i == other.i:
                if self.x == other.x:
                    eq = True  
        return eq


    def delfromgraph(self):
        '''
        metod __del__:  overloads the del operator, so it can be used to delete tracenodes in a graph.
                        This is done in the following way:
                        if self has no parents: self.children is set to an empty list.
                        if self has parents:    self is deleted from the children list of its parents.
        -input:     Tracenode, which is to be deleted from the graph
        -output:    None.
        '''
        if (self.parents==[self] and self.operation=='Id'):
            self.children = []
        else:
            #for k in range(len(Tracenode.Tracenodelist)): #delete node from Tracenodelist.#    if Tracenode.Tracenodelist[k]==self:#       del(Tracenode.Tracenodelist[k])#       break
            for j in range(len(self.parents)):
                for i in range(len(self.parents[j].children)):
                    if self.parents[j].children[i]==self:
                        del(self.parents[j].children[i])
                        break #to avoid an index error, we break from the for-loop, when a child has been deleted from the children list.
        
        
        
        
    





        

class Graph(object):
    '''
    An instance of the class Graph represents a computational graph for a given function evaluation. 
    '''
    def __init__(self, independent, dependent):
        '''
        An object of the class Graph is initialized by a list or array of the independent and 
        a list or array of the dependent variables of a function evaluation. 
        The variables need to be of type Tracenode.
        Attributes:
        -self.independent:      List containing the independent variables of the graph.
        -self.dependent:        List containing the dependent variables of the graph.
        '''
        if type(dependent)==ndarray:
            dependent = dependent.tolist()
        if type(independent)==ndarray:
            independent = independent.tolist()
        if not isinstance(independent, list):
            raise TypeError('The independent variables need to be given in form of a list.')
        if not isinstance(dependent, list):
            raise TypeError('The dependent variables need to be given in form of a list.')
        for i in range(len(independent)):
            if not isinstance(independent[i], Tracenode):
                raise TypeError('The independent variables need to be of type Tracenode.')
        for i in range(len(dependent)):
            if not isinstance(dependent[i], Tracenode):
                raise TypeError('The dependent variables need to be of type Tracenode or an array of Tracenodes.')
        self.independent = independent 
        set_contributesto(array(dependent))
        self.dependent = dependent

        
        
    def __repr__(self):
        printlist = self.independent
        while len(printlist)>0:
            print(printlist[0])
            for i in range(len(printlist[0].children)):
                marker2 = False
                for j in range(len(printlist)):
                    if printlist[0].children[i] == printlist[j]:
                        marker2 = True
                if marker2 == False:
                    printlist = printlist + [printlist[0].children[i]]
            del(printlist[0])
        return '\n-------------------------------------------------\nindependents: \n{}\n-------------------------------------------------\ndependents: \n{}'.format(self.independent,self.dependent)
        
        
        
        
    def optimize(self, depvar):
        '''
        method optimize:    optimizes the given graph by deleting all unnecessary computation steps. 
                            Unnecessary computation steps are those, which do not contribute to the computation of 
                            a given dependent variable.
        -input:         depvar: dependent variable or list/array of dependent variables
                        whose computational graph is to be optimized.
        -output:        None. The given graph is optimized.
        '''
        if type(depvar)==ndarray:
            depvar = depvar.tolist()
        else:
            if isinstance(depvar,Tracenode):
                depvar = [depvar]
        if type(depvar)==list:
            if len(depvar)>self.dependent:
                raise Exception('There are not that many dependent variables in the graph.')
            for i in range(len(depvar)):
                if not isinstance(depvar[i], Tracenode):
                    raise Exception('The dependent variable(s) whose computation is to be optimized need to be of type Tracenode.')
                if not depvar[i] in self.dependent:
                    raise Exception('The variable(s) whose computation is to be optimized need to be dependent variable(s) of the graph.')
        else: 
            raise TypeError('depvar needs to be of type Tracenode or a list of Tracenodes.')
        searchlist = []
        for i in range(len(self.independent)):
            searchlist = searchlist + [self.independent[i]]
            self.independent[i].visited = True
        while len(searchlist)>0:
            node = searchlist[0]
            if len(node.children)>0:
                for j in range(len(node.children)):
                    if node.children[j].visited == False and node.children[j].depth == node.depth +1:
                        searchlist.append(node.children[j])
                        node.children[j].visited = True
            node.contributesto = node.contributesto & set(depvar)
            if len(node.contributesto)==0:
                node.delfromgraph()              
            del(searchlist[0])
        self.dependent = depvar
        setvisitedfalse(self.independent)
        
        
    
    def evaluate(self, indepval):
        '''
        method eval:        with this method, a function whose graph is given, can be evaluated.
                            the program runs through the graph with breadth-first-search.
        -input:         list of new values for the independent variables or 
                        list of independent variables (type tracenode) with the new values
        -output:        dependent variables (self.dependent) with the new function values as attribute .x
        ''' 
        if not isinstance(indepval, list):
            raise TypeError('The independent variables need to be given in form of a list.')
        if len(indepval) != len(self.independent):
            raise Exception('There are {} independent variables!'.format(len(self.independent)))
        if type(indepval[0]) == float or type(indepval[0]) == int:
            for i in range(len(self.independent)):
                self.independent[i].x = indepval[i]
        else:
            if not isinstance(indepval[0], Tracenode):
                raise TypeError('the independent variables need to be given in form of a list of integers/floats or Tracenodes!')
            for j in range(len(self.independent)): 
                indepval[j].i = self.independent[j].i
                indepval[j].contributesto = self.independent[j].contributesto
                indepval[j].children = self.independent[j].children
            self.independent = indepval
        storelist = []
        for i in range(len(self.independent)):
            self.independent[i].visited = True
            for j in range(len(self.independent[i].children)):
                if self.independent[i].children[j].visited == False and self.independent[i].children[j].depth==self.independent[i].depth +1:
                    storelist = storelist + [self.independent[i].children[j]]
                    if self.independent[i].children[j].parents[0].i == self.independent[i].i: # this if/else-statement makes sure, that the children are computed with the new parents..
                        self.independent[i].children[j].parents[0] = self.independent[i]
                    else: 
                        self.independent[i].children[j].parents[1] = self.independent[i]
                    self.independent[i].children[j].visited = True
        while len(storelist)>0:
            node = storelist[0]
            for j in range(len(node.children)):
                if node.children[j].visited == False and node.children[j].depth==node.depth+1:
                    storelist = storelist + [node.children[j]]
                    node.children[j].visited = True
            if len(node.parents)==2:
                if node.operation == 'add':
                    node.x = node.parents[0].x + node.parents[1].x   
                elif node.operation == 'sub':
                    node.x = node.parents[0].x - node.parents[1].x
                elif node.operation == 'div':
                    node.x = node.parents[0].x / node.parents[1].x
                elif node.operation =='mul':
                    node.x = node.parents[0].x * node.parents[1].x
            else:
                if node.operation =='add':
                    node.x = node.parents[0].x + node.opconst
                elif node.operation =='sub':
                    node.x = node.parents[0].x - node.opconst
                elif node.operation == 'mul':
                    node.x = node.parents[0].x * node.opconst
                elif node.operation =='div':
                    node.x = node.parents[0].x / node.opconst
                elif node.operation =='pow':
                    node.x = node.parents[0].x ** node.opconst
                elif node.operation == 'sin':
                    node.x = sin(node.parents[0].x)
                elif node.operation == 'cos':
                    node.x = cos(node.parents[0].x)
                elif node.opareation == 'exp':
                    node.x = exp(node.parents[0].x)
            del(storelist[0])
        setvisitedfalse(self.independent)
        return self.dependent
            
            
            
    def write_c_code(self, filename):
        '''
        method write_c_code:This method creates a c-file called filename.c. 
                            This file contains the c code for the function evaluation.
                            The c code is written while going through the graph as is done in the graph method evaluate.
        -input:         string '... .c': name of the file, which should contain the c code of the function evaluation.
        -output:        None.
        ''' 
        if not type(filename) == str : 
            raise TypeError('Input filename should be a string!')
        if not filename[-1] =='c':
            raise Exception("The filename should be a string that looks like 'name.c'!")
        if not filename[-2] =='.':
            raise Exception("The filename should be a string that looks like 'name.c'!")   
        storelist = []
        ##fehlermeldung für c code einbauen: falls nx bzw. len(self.independent) nicht size(x) entspricht. und gleiches für ny bzw. len(self.dependent) und y.....
        size = 0 # determine number of nodes in the graph aka the size of the field we need in the c code..
        for j in range(len(self.dependent)):
            if self.dependent[j].i > size:
                size = self.dependent[j].i
        size = size +1
        newid = zeros(size,int) # will serve as a map to map the id of the node in the unoptimized graph to a "new fake-id" in the (un)optimized graph
        s = ''
        for i in range(len(self.independent)):
            self.independent[i].visited = True
            s = s +'   v[{}] = x[{}];\n'.format(i, self.independent[i].i)
            for j in range(len(self.independent[i].children)):
                if self.independent[i].children[j].visited == False and self.independent[i].children[j].depth == self.independent[i].depth +1:
                    storelist = storelist + [self.independent[i].children[j]]
                    self.independent[i].children[j].visited = True
            newid[self.independent[i].i] = self.independent[i].i
        for k in range(size-len(self.independent)):            
            if len(storelist)>k:
                node = storelist[k]
                newid[node.i] = k+len(self.independent)
                for j in range(len(node.children)):
                    if node.children[j].visited == False and node.children[j].depth ==node.depth +1:
                        storelist = storelist + [node.children[j]]
                        node.children[j].visited = True
                if len(node.parents)==2:
                    if node.operation == 'add':
                        s = s + '   v[{}] = v[{}] + v[{}];\n'.format(newid[node.i],newid[node.parents[0].i],newid[node.parents[1].i])  
                    elif node.operation == 'sub':
                        s = s + '   v[{}] = v[{}] - v[{}];\n'.format(newid[node.i],newid[node.parents[0].i], newid[node.parents[1].i])
                    elif node.operation == 'div':
                        s = s + '   v[{}] = v[{}] / v[{}];\n'.format(newid[node.i],newid[node.parents[0].i], newid[node.parents[1].i])
                    elif node.operation =='mul':
                        s = s + '   v[{}] = v[{}] * v[{}];\n'.format(newid[node.i],newid[node.parents[0].i], newid[node.parents[1].i])
                else:
                    if node.operation =='add':
                        s = s + '   v[{}] = v[{}] + {};\n'.format(newid[node.i],newid[node.parents[0].i], node.opconst)
                    elif node.operation =='sub':
                        s = s + '   v[{}] = v[{}] - {};\n'.format(newid[node.i],newid[node.parents[0].i], node.opconst)
                    elif node.operation == 'mul':
                        s = s + '   v[{}] = v[{}] * {};\n'.format(newid[node.i],newid[node.parents[0].i], node.opconst)
                    elif node.operation =='div':
                        s = s + '   v[{}] = v[{}] / {};\n'.format(newid[node.i],newid[node.parents[0].i], node.opconst)
                    elif node.operation =='pow':
                        s = s + '   v[{}] = v[{}] ** {};\n'.format(newid[node.i],newid[node.parents[0].i], node.opconst)
                    elif node.operation == 'sin':
                        s = s + '   v[{}] = sin(v[{}]);\n'.format(newid[node.i],newid[node.parents[0].i])
                    elif node.operation == 'cos':
                        s = s + '   v[{}] = cos(v[{}]);\n'.format(newid[node.i],newid[node.parents[0].i])
                    elif node.operation == 'exp':
                        s = s + '   v[{}] = exp(v[{}]);\n'.format(newid[node.i],newid[node.parents[0].i])
                    elif node.operation == 'neg':
                        s = s + '   v[{}] = -v[{}];\n'.format(newid[node.i],newid[node.parents[0].i])
            else:
                break
        for j in range(len(self.dependent)):
            s = s + '   y[{}] = v[{}];\n'.format(j,newid[self.dependent[j].i])
        s = 'void fun(double x[], double y[])\n{\n' + '   double v[{}];\n'.format(newid[size-1]+1)+ s
        s = s + '}'
        setvisitedfalse(self.independent) #we're done. so we set all the visited-attributes back to False
        print(s)
        with open(filename, 'w') as cfile: #write the string in a c-file with name filename
            cfile.write(s)
          
          
            
def setvisitedfalse(nodelist):
    '''
    method setvisitedfalse: sets the attribute visited on False for all nodes in the Graph 
                            which emerges from the nodes in nodelist.
    -input:     list of nodes
    '''
    if not isinstance(nodelist,list):
        raise TypeError(' input for setvisitedfalse needs to be of type list')
    storelist = nodelist
    while len(storelist)>0:
        storelist = storelist + storelist[0].children
        storelist[0].visited = False
        del(storelist[0])
        
            
            
def set_contributesto(result):
    '''
    method set_contributesto:   method can be run after a function of Tracenodes has been evaluated and 
                            thus a Tracenodelist is created. 
                            the method sets the attribute 'contributesto' for all tracenodes of the computation.
                            The method runs through the computational graph using depth-first-search.
    -input:     Tracenode or array of Tracenodes which is the result of a function evaluation.
    -output:    None.
    '''
    if not isinstance(result,Tracenode):
        if not type(result) == ndarray:
            raise TypeError('Input should be a Tracenode or array of Tracenodes.')
        else:
            if not isinstance(result[0],Tracenode):
                raise TypeError('Input should be a Tracenode or array of Tracenodes.')
    #using 'depth-first-search':
    #first, store the result(s) in a list -> easier to handle both cases...
    if type(result)==Tracenode:
        result = [result]
    if type(result)==ndarray:
        result = result.tolist()
    marker  = False # this marker states, if a node which is a result node, but at the same time has children, has been put to the end of storelist in order to postpone the setting of "contributesto"
    storelist=[]
    for i in range(len(result)):
        storelist = storelist + [result[i]] # the store list is a 'waiting list' for all the nodes, that so far only have an empty contributesto-set..
    while (len(storelist)>0):#as long as there are nodes where contributesto has not yet been assigned to:
        node = storelist[0] #take the first node from the top of the list (beginning), this is the current node       
        if node in result:
            node.contributesto = set([node])
            if len(node.children)>0:
                storelist.append(node) # we work with this result node later on
                del(storelist[0])
                node = storelist[0] #take next result node
                if marker == True:
                    for j in range(len(node.children)):
                        node.contributesto = node.contributesto | node.children[j].contributesto
                marker = True
        else:
            for i in range(len(node.children)):
                print(node)
                node.contributesto = node.contributesto | node.children[i].contributesto
                
        del(storelist[0]) #the current node can now be deleted from the 'wating list'
        #now expand and save the parent with the bigger(?) tracernumber as first element of the storelist. we'll deal with this element later..
        if len(node.parents)>1: #
            storelist = [node.parents[1]] + storelist  
        #the parent with the smaller(?) tracernumber is what we concentrate on now.
        ##if we have not yet reached the input-nodes of the function, node.parents[0] becomes the new current node to deal with in the next while loop:
        if not(node.operation=='Id'):
            storelist = [node.parents[0]] + storelist #here, also save the smaller(?) parent in the storelist, but it will be used and deleted right in the beginning of the next while-loop.so this is the current node.
    
    
    
    




def rk_4(fun, y0, (t0,tend)):
    '''rk_4:    solves a differential equation using the classical Runge-Kutte method.
    -input:     fun:        the right hand side of the differential equation which is to be solved
                y0:         initial value of the problem
                (t0,tend):  tuple of the interval borders, the differential equation is considered on.
    -output:    y:          array of size 100, which contains the value of the numerical solution y computed at
                            100 discrete and distinct points of time in the interval [t0,tend], with y[0] being the initial value
                            and y[100] = y[tend].
    '''
    
    
    t0,tend = (t0,tend)
    if t0 > tend:
        raise Exception('t0 needs to be smaller than tend!')
    if t0<0 or tend <= 0:
        raise Exception('t0 and tend need to nonnegative, and tend > 0.')
    #Butcher-Tableau parameters for the classical Runge-Kutta method:
    b = array([1/6, 1/3, 1/3, 1/6])
    c = array([0, 1/2, 1/2, 1])
    A = array([[0,0,0,0], [1/2,0,0,0],[0,1/2,0,0], [0,0,1,0]])
    h = (tend - t0)/3 #constant step size#+#
    t = t0   #initial time
    y = zeros((3,2))#+#
    y[0,:] = y0 # initial value
    k = zeros((4,2)) 
    t = t0
    for i in range(0,2): # we now perform the 100 steps #+#
        t = t + h # perform time step
        for j in range(0,4):
            k[j] = fun(t + h*c[j], y[i] + h*(array([sum(A[j,:]*k[:,0]),sum(A[j,:]*k[:,1])]))) #compute the increments
        y[i+1,:]  = array([y[i,0] + h*sum(b*k[:,0]),y[i,1] + h*sum(b*k[:,1])]) # compute the solution at the current time
    return y
    
    
def rk_4T(fun, y0, (t0,tend)):
    '''rk_4:    solves a differential equation using the classical Runge-Kutte method.
    -input:     fun:        the right hand side of the differential equation which is to be solved
                y0:         initial value of the problem
                (t0,tend):  tuple of the interval borders, the differential equation is considered on.
    -output:    y:          array of size 100, which contains the value of the numerical solution y computed at
                            100 discrete and distinct points of time in the interval [t0,tend], with y[0] being the initial value
                            and y[100] = y[tend].
    '''
    #####statt 100 schritten hier erst mal 3..später ändern!! dort, wo #+# steht
    
    t0,tend = (t0,tend)
    if t0 > tend:
        raise Exception('t0 needs to be smaller than tend!')
    if t0<0 or tend <= 0:
        raise Exception('t0 and tend need to nonnegative, and tend > 0.')
    #Butcher-Tableau parameters for the classical Runge-Kutta method:
    b = array([1/6, 1/3, 1/3, 1/6])
    c = array([0, 1/2, 1/2, 1])
    A = array([[0,0,0,0], [1/2,0,0,0],[0,1/2,0,0], [0,0,1,0]])
    h = (tend - t0)/3 #constant step size #+#
    t = t0   #initial time
    #y1 = [[Tracenode(0.), Tracenode(0.)] for x in range(3)]#+#
    #y = array(y1)    
    #y = zeros((100,2),Tracenode)
    #y[0,:] = y0 # initial value
    #y[0] = y0
    y = [y0]
    #k = array([[Tracenode(0.), Tracenode(0.)] for x in range(4)])
    #print('k')
    #print(k)
    #k = zeros((4,2),Tracenode)
    t = t0
    for i in range(0,2): # we now perform the 100 steps#+#
        k = []
        t = t + h # perform time step
        k.append(fun(t + h*c[0], array([y[-1][0] + h*sum(A[0,:]), y[-1][1] + h*sum(A[0,:])])))
        k.append(fun(t + h*c[1], array([y[-1][0] + h*sum(A[1,0]*k[-1][0]), y[-1][1] + h*sum(A[1,0]*k[-1][1])])))
        k.append(fun(t + h*c[2], array([y[-1][0] + h*sum(A[2,1]*k[-1][0]), y[-1][1] + h*sum(A[2,1]*k[-1][1])])))
        k.append(fun(t + h*c[3], array([y[-1][0] + h*sum(A[3,2]*k[-1][0]), y[-1][1] + h*sum(A[3,2]*k[-1][1])])))        
#        for j in range(0,4):
#            #w4 = zeros(2,Tracenode)
#            #w4 = y[i,:] + h*(array([sum(A[j,:]*k[:,0]),sum(A[j,:]*k[:,1]]))
#            #w4 = array([y[i,0] + h*sum(A[j,:]*k[:,0]), y[i,1] + h*sum(A[j,:]*k[:,1])])
#            #w4[1] = y[i,1] + h*sum(A[j,:]*k[:,1])
#            #k[j] = fun(t + h*c[j], array([y[i,0] + h*sum(A[j,:]*k[:,0]), y[i,1] + h*sum(A[j,:]*k[:,1])])) #compute the increments
#            k[j] = fun(t + h*c[j], array([y[-1][0] + h*sum(A[j,:]*k[:,0]), y[-1][1] + h*sum(A[j,:]*k[:,1])]))
#            print('k[j]')
#            #print(k[j])
        #y[i+1,:]  = array([y[i,0] + h*sum(b*k[:,0]),y[i,1] + h*sum(b*k[:,1])]) # compute the solution at the current time
#        y.append(array([y[-1][0] + h*sum(b*k[:,0]),y[-1][1] + h*sum(b*k[:,1])]))
        k = array(k)
        y.append(array([y[-1][0] + h*sum(b*k[:,0]),y[-1][1] + h*sum(b*k[:,1])]))
        #y.append(array([y[-1][0] + h * sum(b*k[:,0,y[-1][1] + h * sum(b*k[:,1])])]))
    return y
    
def rightside(t,y):
    '''
        rightside gives the right hand side of the Lotka-Volterra-system.
        rs[0] describes the change of the prey at a certain time t
        rs[1] describes the change of the preditor at the same time t.
    -input:     time t, y array, where y[0] is the population of the prey at time t,
                and y[1] is the population of the preditor at time t.
    -output:    right hand side of the model.
    '''
    if not type(y)==ndarray:
        raise TypeError(' y needs to be given in form of an array of dimension 2.')
    if len(y)!=2:
        raise Exception('y is of dimension 2')
    if not isinstance(t,float):
        raise TypeError('time t is of time float..')
    rs = zeros([2])
    rs[0] = y[0] * (100-y[1])
    rs[1] = -y[1] * (100-y[0])
    return rs    
    
def rightsideT(t,y):
    '''
        rightside gives the right hand side of the Lotka-Volterra-system.
        rs[0] describes the change of the prey at a certain time t
        rs[1] describes the change of the preditor at the same time t.
    -input:     time t, y array, where y[0] is the population of the prey at time t,
                and y[1] is the population of the preditor at time t.
    -output:    right hand side of the model.
    '''
    if not type(y)==ndarray:
        raise TypeError(' y needs to be in form of an array of dimension 2.')
    if len(y)!=2:
        raise Exception('y is of dimension 2')
    if not isinstance(t,float):
        raise TypeError('time t is of time float..')
    #rs = zeros([2],Tracenode)
    #rs = array([Tracenode(0.),Tracenode(0.)])
    #rs = array([Tracenode(y[0] * (100-y[1])),Tracenode(-y[1] * (100-y[0]))])
    #rs[1] = -y[1] * (100-y[0])
    return array([y[0] * (100-y[1]),-y[1] * (100-y[0])])
    
    
print(rk_4(rightside,array([200,100]),(0,1)))
a = Tracenode(200.)
b= Tracenode(100.)
v  = rk_4T(rightsideT,array([a,b]),(0,1))
print(v)   
#def qrdecomp(A):
#    if not isinstance(A,ndarray):
#        raise TypeError('Input A needs to be a matrix.')
#    (m,n) = shape(A)    
#    for k in range(n):
#        z = A[k:m,k]
#        uk = z
#        uk[0] = uk[0] + sign(z[0])*norm(z)
#        uk = uk/norm(uk)
#        vk = zeros(m)
#        vk[k:m] = uk
#        A = A - dot((2*vk),(dot(A,vk)))
#    return A
#################################################################################
#################################################################################
#################################################################################        
#u = Tracenode(1.)
#
#v = Tracenode(2.)        
#
#
#def testfunction3(u,v):
#    return u+v+1
#p = testfunction3(u,v)
#print('The result is {} and has tracer number {}.'.format(p.x, p.i))
    
##def testfunction2(w):
##    A = array([[1,0],[0,1]])
##    b = dot(A,w)
##    return b
##    
##l1 = Tracenode(2.)
##l2 = Tracenode(1.)  
##l3 = testfunction2(array([l1,l2]))

##print('The result is [{},{}].'.format(l3[0].x,l3[1].x))
#    
#def testfunction4(u,v):
#    return 2*u*v*2*2*3
#p2 = testfunction4(u,v)
#print('the result is {} and has tracer number {}.'.format(p2.x,p2.i))
#    
#def testfunction5(u,v):
#    return u-v
#p5 = testfunction5(u,v)
#print('the result is {} and has tracer number {}.'.format(p5.x,p5.i))
#    
#def testfunction6(u,v):
#    return v**2-1
#p6 = testfunction6(u,v)
#print('the result is {} and has tracer number {}.'.format(p6.x,p6.i))
#
#    
#def testfunction7(w):
#    A = array([[1,0],[0,1]])
#    B = array([[1,0],[0,1]])
#    return dot(dot(A,B),w)
#    
#p7 = testfunction7(array([l1,l2]))
#print('The result is [{},{}].'.format(p7[0].x,p7[1].x))
#
#def testfunction8():
#    q = Tracenode(0.)
#    r = Tracenode(1.)
#    s = Tracenode(2.)
#    t = Tracenode(3.)
#
#    A = array([[r,s],[q,r]])
#    B = array([[t,r],[r,s]])
#    print(dot(A,B))
#    return dot(A,B)
#
#p8 = testfunction8()
#print('The result is \n[[{},{}],\n [{},{}]].'.format(p8[0][0].x,p8[0][1].x,p8[1][0].x,p8[1][1].x))
