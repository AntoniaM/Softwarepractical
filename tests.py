# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 15:17:47 2014

@author: Antonia
"""
from __future__ import division
from  scipy       import *
from  matplotlib.pyplot import *



tracenode.it = 0
tracenode.othernodelist = []
tracenode.tracenodelist = []
u = tracenode(1.)
v = tracenode(2.) 

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
    
def testfunction8():
    q = tracenode(0.)
    r = tracenode(1.)
    s = tracenode(2.)
    t = tracenode(3.)

    A = array([[r,s],[q,r]])
    B = array([[t,r],[r,s]])
    return dot(A,B)
    
    
    
    
    
    

def test_identity():

    result = testfunction(u,v)
    expected1 = 5.
    assert allclose(result.x,expected1),'Sth went wrong with the computations in function __add__'
    expected2 = 5
    assert allclose(result.i, expected2),'Sth went wrong with the tracing in __add__'
    
    
    tracenode.it = 0
    tracenode.othernodelist = []
    tracenode.tracenodelist = []
    l1 = tracenode(2.)
    l2 = tracenode(1.)
    l3 = testfunction2(array([l1,l2]))
    result = array([l3[0].x,l3[1].x]) 
    expected = array([2,1])
    assert allclose(result,expected),'Sth went wrong with __add__ or __mul__'
    
    
    tracenode.it = 0
    tracenode.othernodelist = []
    tracenode.tracenodelist = []
    u1 = tracenode(1.)
    v1 = tracenode(2.) 
    p2 = testfunction4(u1,v1)
    result = p2.x
    expected = 48.
    assert allclose(result,expected),'Sth went wrong with the computation in __mul__'
    
    result2 = p2.i
    expected2 = 8
    assert allclose(result2,expected2),'Sth went wrong with the tracing in __mul__ '


    tracenode.it = 0
    tracenode.othernodelist = []
    tracenode.tracenodelist = []
    u1 = tracenode(1.)
    v1 = tracenode(2.)
    result = testfunction5(u1,v1)
    expected = -1
    assert allclose(result.x,expected), ' Sth went wrong with the computation in __sub__'
    expected2  = 2
    assert allclose(result.i, expected2), 'Sth went wrong with the tracing in __sub__'
    
    tracenode.it = 0
    tracenode.othernodelist = []
    tracenode.tracenodelist = []
    u1 = tracenode(1.)
    v1 = tracenode(2.)
    result = testfunction6(u1,v1)
    expected = 3
    assert allclose(result.x,expected), ' Sth went wrong with the computation in __pow__or __sub__'
    expected = 4
    assert allclose(result.i, expected), 'Sth went wrong with the tracing in  __pow__ or __sub__'



    tracenode.it = 0
    tracenode.othernodelist = []
    tracenode.tracenodelist = []    
    l1 = tracenode(2.)
    l2 = tracenode(1.)
    result = testfunction7(array([l1,l2]))
    expected = array([l1.x,l2.x])
    assert allclose(array([result[0].x,result[1].x]),expected), 'Sth went wrong with __add__ or __mult__'

    tracenode.it = 0
    tracenode.othernodelist = []
    tracenode.tracenodelist = []
    result = testfunction8()
    expected = array([[5,5],[1,2]])
    assert allclose(array([[result[0][0].x,result[0][1].x],[result[1][0].x, result[1][1].x]]),expected), 'Sth went wrong with __add__ or __mult__'
    expected2 = 15
    maximum = 0
    for i in range(2):
        for j in range(2):
            if maximum<result[i][j].i:
                maximum=result[i][j].i
            
    assert allclose(maximum,15), 'Sth went wrong with the tracing..'









def test_badinput():
    tracenode.it = 0
    try:
        tracenode('a')
    except TypeError:
        pass
    else:
        raise AssertionError('Object can only be created with a float/int as input.')
        
    
    
    
    
    
    
test_identity()    
test_badinput()