# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 15:17:47 2014

@author: Antonia
"""
from __future__ import division
from  scipy       import *
from  matplotlib.pyplot import *



Tracenode.it = 0
Tracenode.othernodelist = []
Tracenode.Tracenodelist = []
u = Tracenode(1.)
v = Tracenode(2.) 

def testfunction(u,v):
    return 1+u+v+1

def testfunction2(w):
    A = array([[1,0],[0,1]])
    return dot(A,w)
    
def testfunction4(u,v):
    return 2*u*v*2*2*3 
    
def testfunction5(u,v):
    return u-v

def testfunction6(u,v):
    return v**2-1
    
def testfunction7(w):
    A = array([[1,0],[0,1]])
    B = array([[1,0],[0,1]])
    return dot(dot(A,B),w)
    
#def testfunction8(w):
 #   A = array([[1,2],[0,1]])
  #  B = array([[3,1],[1,2]])
   # return dot(A,B)*w
    
def testfunction9(x):
    return array([x[0]+x[1],x[1],x[0]])
    
    
    
    

def test_identity():

    result = testfunction(u,v)
    expected1 = 5.
    assert allclose(result.x,expected1),'Sth went wrong with the computations in function __add__' 
    expected2 = 4
    assert allclose(result.i, expected2),'Sth went wrong with the tracing in __add__'
    
    
    Tracenode.it = 0
    l1 = Tracenode(2.)
    l2 = Tracenode(1.)
    l3 = testfunction2(array([l1,l2]))
    result = array([l3[0].x,l3[1].x]) 
    expected = array([2,1])
    assert allclose(result,expected),'Sth went wrong with __add__ or __mul__'
    
    #test function set_contributesto
    g = Graph([l1,l2],l3)
    result = g.dependent[0].contributesto
    expected = set([g.dependent[0]])
    if result != expected:
        raise Exception('Sth went wrong with the set_contributes method or graph of testfunction2')
        
    result = g.dependent[0].parents[0].contributesto
    if len(result & set([g.dependent[0]])) == 0:
        raise Exception('Sth went wrong with the set_contributes method or graph for testfunction2')
        
    #test function setvisitedfalse:
    l4 = Tracenode(3.)
    l4.visited = True
    setvisitedfalse([l4],'up')
    if l4.visited == True:
        raise Exception('Method setvisitedfalse did not work the way it should..')
    
    
    #test function evaluate:
    result = g.evaluate([0,30])
    result[0] = result[0].x
    result[1] = result[1].x
    expected  = array([0,30])
    if result[0] != expected[0]:
        raise Exception("Graph method 'evaluate' did not work the way it should..")
    if result[1] != expected[1]:
        raise Exception("Graph method 'evaluate' did not work the way it should..")
        
    l5 = array([Tracenode(10.),Tracenode(20.)])
    result = testfunction7(l5)
    if result[0].x != 10.:
        raise Exception("Graph method 'evaluate' did not work the way it should..")
    if result[1].x != 20.:
        raise Exception("Graph method 'evaluate' did not work the way it should..")
        
        

    
    
    Tracenode.it = 0
    u1 = Tracenode(1.)
    v1 = Tracenode(2.) 
    p2 = testfunction4(u1,v1)
    result = p2.x
    expected = 48.
    assert allclose(result,expected),'Sth went wrong with the computation in __mul__'
    
    result2 = p2.i
    expected2 = 6
    assert allclose(result2,expected2),'Sth went wrong with the tracing in __mul__ '


    Tracenode.it = 0
    u1 = Tracenode(1.)
    v1 = Tracenode(2.)
    result = testfunction5(u1,v1)
    expected = -1
    assert allclose(result.x,expected), ' Sth went wrong with the computation in __sub__'
    expected2  = 2
    assert allclose(result.i, expected2), 'Sth went wrong with the tracing in __sub__'
    
    Tracenode.it = 0
    u1 = Tracenode(1.)
    v1 = Tracenode(2.)
    result = testfunction6(u1,v1)
    expected = 3
    assert allclose(result.x,expected), ' Sth went wrong with the computation in __pow__or __sub__'
    expected = 3
    assert allclose(result.i, expected), 'Sth went wrong with the tracing in  __pow__ or __sub__'



    Tracenode.it = 0
    l1 = Tracenode(2.)
    l2 = Tracenode(1.)
    result = testfunction7(array([l1,l2]))
    expected = array([l1.x,l2.x])
    assert allclose(array([result[0].x,result[1].x]),expected), 'Sth went wrong with __add__ or __mult__'

#    Tracenode.it = 0
 #   Tracenode.othernodelist = []
  #  Tracenode.Tracenodelist = []
#    w = Tracenode(1)
 #   result = testfunction8(w)
  #  expected = array([[5,5],[1,2]])
#    assert allclose(array([[result[0][0].x,result[0][1].x],[result[1][0].x, result[1][1].x]]),expected), 'Sth went wrong with __add__ or __mult__'
 #   expected2 = 16
  #  maximum = 0
#    for i in range(2):
 #       for j in range(2):
  #          if maximum<result[i][j].i:
   #             maximum=result[i][j].i
   # print(maximum)       
    #assert allclose(maximum,expected2), 'Sth went wrong with the tracing..'


    Tracenode.it = 0
    Tracenode.Tracenodelist = []
    x = array([Tracenode(1),Tracenode(1)])
    result = testfunction9(x)
###    print(result)
    expected = array([2,1,1])
    assert allclose(array([result[0].x,result[1].x,result[2].x]),expected), 'sth went wrong in testfunction9'
    






def test_badinput():
    Tracenode.it = 0
    try:
        Tracenode('a')
    except TypeError:
        pass
    else:
        raise AssertionError('Object can only be created with a float/int as input.')
        
    
    
    
    
    
    
test_identity()    
test_badinput()