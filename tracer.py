# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 17:18:50 2014

@author: Antonia
"""
from __future__ import division
from  scipy       import *
from  matplotlib.pyplot import *


class tracenode(object):  
    '''
    An object of the class represents a node in a computational graph for a function.
    '''
    it = 0 # serves as counter for the instances created..
    ###othernodelist = []
    tracenodelist = []  #in this list, all the created instances will be stored
    storelist = [] #the storelist will be used when setting the attribute 'active' of active tracenode instances to 'True'
        
        
    def __init__(self, x):
        '''
        The class tracenode is initialized with a float or integer, the actual value of the node which is created.
        Attributes:
        -self.x:        actual value of the node
        -self.i:        id-number of the node
        -self.origin:   list, containing the nodes, the created node is computed of
        -self.active:   states, if the node playes an active role when evaluating the function. default value: False. To see if a node is active or not, the method 'setallactive' needs to be run after a function has been evaluated.
        -self.operation:states the operation self.x arises out of        
        '''
        if not isinstance(x, float):
            if isinstance(x,int):
                x = float(x)
            else:
                raise TypeError('input argument of function needs to be a float.')
        self.x = x 
        self.i = tracenode.it
        self.origin = [self.i] #if the created tracenode is a result of an operation, then self.origin will be set to the corresponding origin indices while the operation is executed..
        ########## self._origin + get/set methoden?????????? weil origin bei durchführen einer Operation verändert wird...
        self.active = False #Mittels Tiefensuche wird später festgestellt, ob object active ist oder nicht...default-value: False.        
        self.operation = 'Id' #Default value: Identity function        
        self.opconst = None #states, if the operation was performed using a constant
        tracenode.it = tracenode.it+1
        tracenode.tracenodelist.append(self) #stores all the during a function evaluation created objects of type tracenode in a list.


    def __repr__(self):
        return ' tracer number {} \torigin{} \toperation {}\t with const. {}\tactive: {}\tvalue {}\n'.format(self.i,self.origin,self.operation,self.opconst, self.active,self.x)
        
        
    def __add__(self, other):
        '''
        method __add__:     overloads the add operator, so it can be used for data of type tracenode. 
                            works for the addition of data of type tracenodes, 
                            tracenode and integer, tracenode and float. and vice versa.
        -input:     tracenode, tracenode/integer/float
        -output:    tracenode addit, where addit.x contains the value of the addition, 
                    addit.origin contains a list of the tracenumbers of the summands,
                    addit.operation states, that addit was created by an addition
        '''
        if not isinstance(other, tracenode):        #for v+2 e.g., we first look, if there already was a node created for this 2 or if we have to create a new one...            
            if isinstance(other, int):
                other = float(other)
            else: 
                raise TypeError('Addition is only defined for types tracenode and tracenode or float or int.')
            addit = tracenode(self.x + other)     
            addit.opconst = other
            addit.origin = [self.i]      
        else:
            addit = tracenode(self.x + other.x)          
            addit.origin = [self.i, other.i]
        addit.operation = 'add'
        return addit


        
    def __radd__(self,other):
        return self+other
    
    
    def __sub__(self, other):
        '''
        method __sub__:     overloads the sub operator, so it can be used for data of type tracenode.
                            works for the subtraction of data of type tracenodes,
                            tracenode and integer, tracenode and float. and vice versa.
        -input:     tracenode, tracenode/integer/float
        -output:    tracenode subtr, where subtr.x contains the value of the subtraction,
                    subtr.origin contains a list of the tracenumbers of the summands
        '''
        if not isinstance(other, tracenode):        #for v+2 e.g., we first look, if there already was a node created for this 2 or if we have to create a new one...            
            if isinstance(other, int):
                other = float(other)
            else: 
                raise TypeError('Subtraction is only defined for types tracenode and tracenode or float or int.')
            subtr = tracenode(self.x - other)     
            subtr.opconst = other
            subtr.origin = [self.i]      
        else:
            subtr = tracenode(self.x - other.x)     
            subtr.origin = [self.i, other.i]
        subtr.operation = 'sub' 
        return subtr
        
            
    def __mul__(self, other):
        '''method __mul__:  overloads the mul operator, so it can be used for data of type tracenode.
                            works for the multiplication of data of type tracenodes,
                            tracenode and integer, tracenode and float. and vice versa.
        -input:     tracenode, tracenode/integer/float
        -output:    tracenode multip, where multip.x contains the resultvalue of the multiplication,
                    multip.origin contains a list of the tracenumbers of the factors.
        '''
        if not isinstance(other, tracenode):        #for v+2 e.g., we first look, if there already was a node created for this 2 or if we have to create a new one...            
            if isinstance(other, int):
                other = float(other)
            else: 
                raise TypeError('Multiplication is only defined for types tracenode and tracenode or float or int.')
            multip = tracenode(self.x * other)     
            multip.opconst = other
            multip.origin = [self.i]      
        else:
            multip = tracenode(self.x + other.x)
            multip.origin = [self.i, other.i]
        multip.operation = 'mul'        
        return multip
        
#        if not isinstance(other, tracenode):
#            if isinstance(other, int):
#                other = float(other)
#            if isinstance(other, float):             
#                for j in range(len(tracenode.othernodelist)):
#                    if tracenode.othernodelist[j].x==other:
#                        j=j+1
#                        break
#                else:
#                    othernode = tracenode(other)
#                    tracenode.othernodelist.append(othernode) #wird für eine zahl, z.b. bei u+2 2 als neuer knoten bestimmt und dann von den knoten u und 2 aus u+2 berechnet?oder ist da nur u ein knoten?
#                    j = len(tracenode.othernodelist)
#                multip = tracenode(self.x*tracenode.othernodelist[j-1].x)
#                multip.origin = [self.i,tracenode.othernodelist[j-1].i]
#                print('multiplication of {} and {} let to {}.'.format(self.i, tracenode.othernodelist[j-1].i, multip.i))
#                return multip
#            else:
#                raise TypeError('Multiplication is only defined for types tracenode or float or int.')
#        multip = tracenode(self.x*other.x)
#        multip.origin = [self.i,other.i]
#        print('multiplication of {} and {} let to {}.'.format(self.i, other.i,multip.i))
#        return multip
        
        
    def __rmul__(self,other):
        return self*other
        
        
    def __div__(self,other):
        '''method __div__:  overloads the div operator, so it can be used for data of type tracenode.
                            works for the division of data of type tracenodes,
                            tracenode and integer, tracenode and float. and vice versa.
        -input:     tracenode, tracenode/integer/float
        -output:    tracenode divis, where divis.x contains the resultvalue of the division,
                    divis.origin contains a list of the tracenumbers of the factors.
        '''
        if not isinstance(other, tracenode):        #for v+2 e.g., we first look, if there already was a node created for this 2 or if we have to create a new one...               
            if other ==0:
                raise ZeroDivisionError('Division by Zero not possible')
            if isinstance(other, int):
                other = float(other)
            else: 
                raise TypeError('Division is only defined for types tracenode and tracenode or float or int.')
            divis = tracenode(self.x / other)     
            divis.opconst = other
            divis.origin = [self.i]      
        else:
            divis = tracenode(self.x / other.x)       
            divis.origin = [self.i, other.i]
        divis.operation = 'div'
        return divis
        
#        if not isinstance(other, tracenode):
#            if other==0:
#                raise ZeroDivisionError('Division by Zero not possible.')
#            if isinstance(other, int):
#                other = float(other)
#            if isinstance(other, float):             
#                for j in range(len(tracenode.othernodelist)):
#                    if tracenode.othernodelist[j].x==other:
#                        j=j+1
#                        break
#                else:
#                    othernode = tracenode(other)
#                    tracenode.othernodelist.append(othernode) #wird für eine zahl, z.b. bei u+2 2 als neuer knoten bestimmt und dann von den knoten u und 2 aus u+2 berechnet?oder ist da nur u ein knoten?
#                    j = len(tracenode.othernodelist)
#                divis = tracenode(self.x/tracenode.othernodelist[j-1].x)
#                divis.origin = [self.i,tracenode.othernodelist[j-1].i]
#                print('division of {} and {} let to {}.'.format(self.i, tracenode.othernodelist[j-1].i, divis.i))
#                return divis
#            else:
#                raise TypeError('Division is only defined for types tracenode or float or int.')
#        if other.x==0:
#            raise ZeroDivisionError
#        divis = tracenode(self.x/other.x)
#        divis.origin = [self.i,other.i]
#        print('division of {} and {} let to {}.'.format(self.i, other.i,divis.i))
#        return divis
        
        
    def __pow__(self, other):
        '''
        method __pow__: overloadsthe pow operator, so it can be used for data of type tracenode.
                        data of type tracenodes can be taken to the power of data of type integers.
        -input:     tracenode, integer
        -output:    tracenode power, where power.x contains the value of the tracenodevalue to the power of the integer,
                    power.origin contains a list (with only one element) of the tracenumber of the tracenode, 
                    which is taken to the power of the integer..
        '''
        if not isinstance(other, int):
            raise TypeError('function power is only defined for to the power of integers.')
        power = tracenode(self.x**other)
        power.origin = [self.i]
        power.operation = 'pow'
        power.opconst = other
        return power
    



    
def setallactives(result):
    '''
    method setallactives:   method can be run after a function of tracenodes has been evaluated and 
                            thus a tracenodelist is created. 
                            the method sets the attribute 'active' on 'True' for all tracenode instances, 
                            which play an active role in the computation of the value of the function.
                            Meaning those, which were actually needed in order to compute the final function value.
                            The method runs through the computational graph using depth-first-search.
    -input:     tracenode which is the result of a function evaluation.
    -output:    none.
    '''
    #using 'depth-first-search':
    #first, store the result(s) in a list->easier to handle both cases...
    if type(result)==tracenode:
        result = [result]
    if type(result)==ndarray:
        result = result.tolist()
    ##########wrong input exception einfügen!!
    storelist = result # the store list is a 'waiting list' for all the nodes, that wait to be activated..
    while (len(storelist)>0):#as long as there are nodes node tested yet:
        node = storelist[0] #take the first node from the top of the list (beginning), this is the current node
        node.active = True
        del(storelist[0]) #the current node can now be deleted from the 'wating list'
        #now expand and save the bigger origin as first element of the storelist.we'll deal with this element later..
        if len(node.origin)>1: #
            storelist = [tracenode.tracenodelist[node.origin[1]]] + storelist   
        smallnode  = tracenode.tracenodelist[node.origin[0]]  #the small origin is what we concentrate on now.
        #if the small has not yet become activated, it becomes the new current node for the next while loop
        if smallnode.active == False:
            storelist = [smallnode] + storelist #here, also save the smaller origin in the storelist, but it will be used and deleted right in the beginning of the next while-loop.so this is the current node.

        
        
        
        
        
        
        
        
        
        
#################################################################################
#################################################################################
#################################################################################        
#u = tracenode(1.)

#v = tracenode(2.)        


#def testfunction3(u,v):
#    return u+v+1
#p = testfunction3(u,v)
#print('The result is {} and has tracer number {}.'.format(p.x, p.i))
    
def testfunction2(w):
    A=array([[1,0],[0,1]])
    return dot(A,w)
    
l1 = tracenode(2.)
l2 = tracenode(1.)  
l3 = testfunction2(array([l1,l2]))
##print('The result is [{},{}].'.format(l3[0].x,l3[1].x))
    
#def testfunction4(u,v):
#    return 2*u*v*2*2*3
#p2 = testfunction4(u,v)
#print('the result is {} and has tracer number {}.'.format(p2.x,p2.i))
    
#def testfunction5(u,v):
#    return u-v
#p5 = testfunction5(u,v)
#print('the result is {} and has tracer number {}.'.format(p5.x,p5.i))
    
#def testfunction6(u,v):
#    return v**2-1
#p6 = testfunction6(u,v)
#print('the result is {} and has tracer number {}.'.format(p6.x,p6.i))

    
#def testfunction7(w):
#    A = array([[1,0],[0,1]])
#    B = array([[1,0],[0,1]])
#    return dot(dot(A,B),w)
    
#p7 = testfunction7(array([l1,l2]))
#print('The result is [{},{}].'.format(p7[0].x,p7[1].x))

#def testfunction8():
#    q = tracenode(0.)
#    r = tracenode(1.)
#    s = tracenode(2.)
#    t = tracenode(3.)
#
#    A = array([[r,s],[q,r]])
#    B = array([[t,r],[r,s]])
#    print(dot(A,B))
#    return dot(A,B)

#p8 = testfunction8()
#print('The result is \n[[{},{}],\n [{},{}]].'.format(p8[0][0].x,p8[0][1].x,p8[1][0].x,p8[1][1].x))



    