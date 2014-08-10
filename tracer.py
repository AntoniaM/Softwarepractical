# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 17:18:50 2014

@author: Antonia
"""
from __future__ import division
from  scipy       import *
from  matplotlib.pyplot import *


class tracenode(object):
    it = 0
    othernodelist = []
    tracenodelist = []
        
    def __init__(self, x):
        if not isinstance(x, float):
            if isinstance(x,int):
                x = float(x)
            else:
                raise TypeError('inputargument of function needs to be a float.')
        self.x = x
        self.i = tracenode.it
        self.origin = [self.i] #if the created tracenode is a result of an operation, then self.origin will be set to the corresponding origin indices while the operation is executed..
        ##### self._origin + get/set methoden?????????? weil origin bei durchführen einer Operation verändert wird...
        self.active = False #Mittels Tiefensuche wird später festgestellt, ob object active ist oder nicht...default-value: False.        
        print('created new object with tracer number {}'.format(self.i))
        tracenode.it = tracenode.it+1
        tracenode.tracenodelist.append(self) #stores all the during a function evaluation created objects of type tracenode in a list.


    def __repr__(self):
        return ' tracer number {} \torigin {}\tactive: {}\tvalue {}\n'.format(self.i,self.origin,self.active,self.x)
        
        
    def __add__(self, other):
        if not isinstance(other, tracenode):        #for v+2 e.g., we first look, if there already was a node created for this 2 or if we have to create a new one...            
            if isinstance(other, int):
                other = float(other)
            if isinstance(other, float):             
                for j in range(len(tracenode.othernodelist)):
                    if tracenode.othernodelist[j].x==other:
                        j=j+1
                        break                    
                else:
                    othernode = tracenode(other)
                    tracenode.othernodelist.append(othernode) #wird für eine zahl, z.b. bei u+2 2 als neuer knoten bestimmt und dann von den knoten u und 2 aus u+2 berechnet?oder ist da nur u ein knoten?
                    j = len(tracenode.othernodelist)
                addit = tracenode(self.x + tracenode.othernodelist[j-1].x)
                addit.origin = [self.i,tracenode.othernodelist[j-1].i]
                print('addition of {} and {} let to {}.'.format(self.i,tracenode.othernodelist[j-1].i,addit.i))
                return addit
            else:
                raise TypeError('Addition is only defined for types tracenode or float or int.')
        addit = tracenode(self.x + other.x)
        addit.origin = [self.i,other.i]
        print('addition of {} and {} let to {}.'.format(self.i,other.i,addit.i))
        return addit

        
    def __radd__(self,other):
        return self+other
    
    
    def __sub__(self, other):
        if not isinstance(other, tracenode):        #for v+2 e.g., we first look, if there already was a node created for this 2 or if we have to create a new one...            
            if isinstance(other, int):
                other = float(other)
            if isinstance(other, float):             
                for j in range(len(tracenode.othernodelist)):
                    if tracenode.othernodelist[j].x==other:
                        j=j+1
                        break                    
                else:
                    othernode = tracenode(other)
                    tracenode.othernodelist.append(othernode) #wird für eine zahl, z.b. bei u+2 2 als neuer knoten bestimmt und dann von den knoten u und 2 aus u+2 berechnet?oder ist da nur u ein knoten?
                    j = len(tracenode.othernodelist)
                subtr = tracenode(self.x - tracenode.othernodelist[j-1].x)
                subtr.origin = [self.i,tracenode.othernodelist[j-1].i]
                print('subtraction of {} and {} let to {}.'.format(self.i,tracenode.othernodelist[j-1].i,subtr.i))
                return subtr
            else:
                raise TypeError('Subtraction is only defined for types tracenode or float or int.')
        subtr = tracenode(self.x - other.x)
        subtr.origin = [self.i,other.i]
        print('subtraction of {} and {} let to {}.'.format(self.i,other.i,subtr.i))
        return subtr
        
            
    def __mul__(self, other):
        if not isinstance(other, tracenode):
            if isinstance(other, int):
                other = float(other)
            if isinstance(other, float):             
                for j in range(len(tracenode.othernodelist)):
                    if tracenode.othernodelist[j].x==other:
                        j=j+1
                        break
                else:
                    othernode = tracenode(other)
                    tracenode.othernodelist.append(othernode) #wird für eine zahl, z.b. bei u+2 2 als neuer knoten bestimmt und dann von den knoten u und 2 aus u+2 berechnet?oder ist da nur u ein knoten?
                    j = len(tracenode.othernodelist)
                multip = tracenode(self.x*tracenode.othernodelist[j-1].x)
                multip.origin = [self.i,tracenode.othernodelist[j-1].i]
                print('multiplication of {} and {} let to {}.'.format(self.i, tracenode.othernodelist[j-1].i, multip.i))
                return multip
            else:
                raise TypeError('Multiplication is only defined for types tracenode or float or int.')
        multip = tracenode(self.x*other.x)
        multip.origin = [self.i,other.i]
        print('multiplication of {} and {} let to {}.'.format(self.i, other.i,multip.i))
        return multip
    #def __dot__(self,other):???? oder wird beim aufrufen  von dot ja eh auf add, mult etc zurückgegriffen und deshalb braucht man dot gar nicht mehr zu überladen..?
        
        
    def __rmul__(self,other):
        return self*other
        
        
    def __div__(self,other):
        if not isinstance(other, tracenode):
            if other==0:
                raise ZeroDivisionError('Division by Zero not possible.')
            if isinstance(other, int):
                other = float(other)
            if isinstance(other, float):             
                for j in range(len(tracenode.othernodelist)):
                    if tracenode.othernodelist[j].x==other:
                        j=j+1
                        break
                else:
                    othernode = tracenode(other)
                    tracenode.othernodelist.append(othernode) #wird für eine zahl, z.b. bei u+2 2 als neuer knoten bestimmt und dann von den knoten u und 2 aus u+2 berechnet?oder ist da nur u ein knoten?
                    j = len(tracenode.othernodelist)
                divis = tracenode(self.x/tracenode.othernodelist[j-1].x)
                divis.origin = [self.i,tracenode.othernodelist[j-1].i]
                print('division of {} and {} let to {}.'.format(self.i, tracenode.othernodelist[j-1].i, divis.i))
                return divis
            else:
                raise TypeError('Division is only defined for types tracenode or float or int.')
        if other.x==0:
            raise ZeroDivisionError
        divis = tracenode(self.x/other.x)
        divis.origin = [self.i,other.i]
        print('division of {} and {} let to {}.'.format(self.i, other.i,divis.i))
        return divis
        
        
    def __pow__(self, other):
        if not isinstance(other, int):
            raise TypeError('function power is only defined for to the power of integers.')
        power = tracenode(self.x**other)
        power.origin = [self.i]
        print('taken value with tracer number {} to the power of {} let to result with tracer number {}.'.format(self.i,other,power.i))
        return power
    
        
        
#################################################################################
#################################################################################
        
u = tracenode(1.)

v = tracenode(2.)        
        
def testfunction(u,v):
    w=1.
    #t = v+w
    t = w+v
    o= t+w
    return u+o

def testfunction3(u,v):
    return u+v+1
#p = testfunction3(u,v)
#print('The result is {} and has tracer number {}.'.format(p.x, p.i))
    
def testfunction2(w):
    A=array([[1,0],[0,1]])
    return dot(A,w)
    
#l1 = tracenode(2.)
#l2 = tracenode(1.)  
#l3 = testfunction2(array([l1,l2]))
#print('The result is [{},{}].'.format(l3[0].x,l3[1].x))
    
def testfunction4(u,v):
    return 2*u*v*2*2*3
#p2 = testfunction4(u,v)
#print('the result is {} and has tracer number {}.'.format(p2.x,p2.i))
    
def testfunction5(u,v):
    return u-v
#p5 = testfunction5(u,v)
#print('the result is {} and has tracer number {}.'.format(p5.x,p5.i))
    
def testfunction6(u,v):
    return v**2-1
p6 = testfunction6(u,v)
print('the result is {} and has tracer number {}.'.format(p6.x,p6.i))

    
def testfunction7(w):
    A = array([[1,0],[0,1]])
    B = array([[1,0],[0,1]])
    return dot(dot(A,B),w)
    
#p7 = testfunction7(array([l1,l2]))
#print('The result is [{},{}].'.format(p7[0].x,p7[1].x))

def testfunction8():
    q = tracenode(0.)
    r = tracenode(1.)
    s = tracenode(2.)
    t = tracenode(3.)

    A = array([[r,s],[q,r]])
    B = array([[t,r],[r,s]])
    print(dot(A,B))
    return dot(A,B)

#p8 = testfunction8()
#print('The result is \n[[{},{}],\n [{},{}]].'.format(p8[0][0].x,p8[0][1].x,p8[1][0].x,p8[1][1].x))



    