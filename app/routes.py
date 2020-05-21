from flask import render_template, request, redirect
from app import app

import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial
from scipy.interpolate import lagrange

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/regla-trapecio')
def trapecio():
    return render_template('trapecio.html', title='Trapecio')

@app.route('/resulTrapecio', methods=['POST'])
def resulTrapecio():
    
    limInf   = request.form.get("limInf", type=float)
    limSup   = request.form.get("limSup", type=float)
    numIter  = request.form.get("numIter", type=int)
 ####################### AQUI VA LA FUNCION DE TRAPECIO ##############################   
    def function(x):
        return 8+4*math.cos(x)
    if numIter == 2:
        h = (limSup - limInf) / 2
        integral = (function(limInf) + function(limSup))
        integral *= h
    else :
        h = (limSup - limInf) / numIter
        integral = (function(limInf) + function(limSup))
        print("La integrando solo a  y b : es {}".format(integral) )
    for i in range(1,numIter):
        integral += 2*(function(limInf + h * i))
        integral *= h/2
    integralString = str(integral)
    return render_template('result-trapecio.html', integralString=integralString, title='Resultado Trapecio')

@app.route('/lagrange')
def lagrangePage():
    return render_template('lagrange.html', title='Lagrange')

@app.route('/resultLagrange', methods=['POST'])
def resultLagrange():
    listax = []
    listay = []
    n = int(input("Ingrese el valor de n+1: ")) 
    for i in range (n):
        valor =  int(input("ingrese el valor {} de x: ".format(i)))
        listax.append(valor)
    for i in range (n):
        valor =  int(input("ingrese el valor {} de y: ".format(i)))
        listay.append(valor)

    x = np.array(listax)
    y = np.array(listay)

    poly = lagrange(x,y)

    polyString = str(poly)
    return render_template('result-lagrange.html', title='Resultado Lagrange',polyString = polyString)

@app.route('/simpson-tercio')
def simpsonTercios():
    return render_template('simpson-tercio.html', title='Simpson Tercio')

@app.route('/resultSimpsonTercio',methods=['POST'])
def resultSimpsonTercio():
    limInf   = request.form.get("limInf", type=float)
    limSup   = request.form.get("limSup", type=float)
    numIter  = request.form.get("numIter", type=int)
################################# AQUI VA SIMPSON 1/3 #############################
    def function(x):
        return x/(4+x*x)
    h = (limInf - limSup)/numIter
    k = h/3
    integral = function(limInf) + function(limSup)
    for i in range (numIter - 1):
        if (i%2==0):
            integral += 2*(function(limInf + h*i))
        else:
            integral += 4*(function(limInf + h*i))
    integral *= -h/3
    integralString = str(integral)
    return render_template('result-simpson-tercio.html', integralString=integralString, title='Resultado Simpson 1/3')
