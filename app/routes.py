from flask import render_template, request, redirect
from app import app

import math
import numpy as np
# import sympy as sy
import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial
from scipy.interpolate import lagrange
from scipy import interpolate

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/regla-trapecio')
def trapecio():
    return render_template('trapecio.html', title='Trapecio')

@app.route('/resulTrapecio', methods=['POST'])
def resulTrapecio():
    funcion  = request.form.get("funcion", type=str)
    limInf   = request.form.get("limInf", type=float)
    limSup   = request.form.get("limSup", type=float)
    numIter  = request.form.get("numIter", type=int)
  
    def function(x):
        return eval(funcion)
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
        valor =  float(input("ingrese el valor {} de x: ".format(i)))
        listax.append(valor)
    for i in range (n):
        valor =  float(input("ingrese el valor {} de y: ".format(i)))
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
    funcion  = request.form.get("funcion", type=str)
    limInf   = request.form.get("limInf", type=float)
    limSup   = request.form.get("limSup", type=float)
    numIter  = request.form.get("numIter", type=int)

    def function(x):
        return eval(funcion)
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

@app.route('/simpsonTercioDos')
def simpsonTercioDos():
    return render_template('tercioDos.html', title='Simpson Tercio(2)')

@app.route('/resultSimpsonTercio-dos',methods=['POST'])
def resultSimpsonTercioDos():
    n = int(input("Ingrese el valor de n +1: "))
    listaX = []
    listaY = []
    for i in range (n):
        val =  float(input("ingrese el valor {} de x: ".format(i)))
        listax.append(val)
    for i in range (n):
        val_1 = float(input("ingrese el valor {} de y: ".format(i)) )
        listaY.append(val_1)


    h = (listaX[n-1] - listaX[0])/(n-1)

    k = h/3

    integral = listaY[0]+listaY[n-1]

    for i in range (1,n-1):
        if (i%2==0):
            integral += 2*listaY[i]
            print("valor multiplicado por 2", 2*listaY[i] )
    else:
        integral += 4*listaY[i]
        print("valor multiplicado por 4", 4*listaY[i] )
    integral *= k
    integralString = str(integral)
    return render_template('resultSimpsonDos.html', integralString=integralString, title='Resultado Simpson 1/3 (2)')

@app.route('/splines-cubicos')
def splineCubico():
    return render_template('splines-cubicos.html', title='Splines Cubicos')

@app.route('/resultCubicos',methods=['POST'])
def resultCubicos():
    efedequis = request.form.get("efedequis", type=float)
    tamanoListas = request.form.get("tamanoListas", type=int)

    def f(x):
        listaX = []
        listaY = []
        for i in range (tamanoListas):
            valor =  float(input("ingrese el valor {} de x: ".format(i)))
            listaX.append(valor)
        for i in range (tamanoListas):
            val_1 = float(input("ingrese el valor {} de y: ".format(i)))
            listaY.append(val_1)
        tck = interpolate.splrep(listaX, listaY)
        return interpolate.splev(x, tck)

    resultadoStr = str(f(efedequis))

    return render_template('result-cubicos.html',resultadoStr=resultadoStr, title='Resultado Cubicos')

@app.route('/polinomioNewton')
def polinomioNewton():
    return render_template('polinomioNewton.html', title="Formula de Newton")
    
@app.route('/resultNewton',methods=['POST'])
def resultNewton():
    gradoPoli = request.form.get("gradoPoli", type=int)
    puntoBusqueda = request.form.get("puntoBusqueda", type=float)
        
    matriz = [0.0] * gradoPoli
    for i in range(gradoPoli):
        matriz[i] = [0.0] * gradoPoli
        
    vector = [0.0] * gradoPoli

    for i in range(gradoPoli):
        x = input("Ingrese el valor de x: ")
        y = input("Ingrese el valor de f("+x+"): ")
        vector[i]=float(x)
        matriz[i][0]=float(y)

    for i in range(1,gradoPoli):
        for j in range(i,gradoPoli):
            matriz[j][i] = ( (matriz[j][i-1]-matriz[j-1][i-1]) / (vector[j]-vector[j-i]))
    
    aprx = 0
    mul = 1.0
    for i in range(gradoPoli):
        mul = matriz[i][i]
    for j in range(1,i+1):
        mul = mul * (puntoBusqueda - vector[j-1])
    aprx = aprx + mul

    aprxStr = str(aprx)

    return render_template('resultadoNewton.html', aprxStr=aprxStr, title='Resultado Newton')
