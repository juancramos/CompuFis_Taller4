import sys
import string
import os
import numpy
import scipy
from pylab import *
from scipy.optimize import curve_fit
from scipy.linalg import *

#Crear un archivo con la lista de los nombres

cwd = os.getcwd()
lista_archivos = os.listdir('hw4_data/')
nombres = open("nombres", 'w+')

for nombre in lista_archivos:
    nombres.write("%s\n"%nombre)
nombres.close()


#Archivo que contiene los parametros

data = open("data.dat",'w')
data_table = []
data_table_pca = []

 
#Calculo de parametros

names=open("nombres",'r')
lista =names.readlines()
num_lineas=len(lista)

for i in range(num_lineas):

    nombre=lista[i]
    nombre=nombre.replace('\n','')
    t,x,y = numpy.loadtxt('hw4_data/'+nombre, skiprows=2, unpack=True)

    #Fit de los datos
    x_fit = numpy.polyfit(t, x, 1.0)
    y_fit = numpy.polyfit(t, y, 2.0)
    vx = float(x_fit[0])
    vy = float(y_fit[1])
    g = -2*float(y_fit[0])
    
    #Metodo para extraer el angulo y el ID a partir del nombre del archivo
    info = (nombre.replace('.dat','')).split('_')
    angulo = float(info[3])
    iden = int(info[1])
    
    #Lista de tuplas. Cada tupla corresponde a (id, angulo, velocidad_x, velocidad_y, g)
    data_table.append((iden, angulo, vx, vy, g))
    data_table_pca.append((vx, vy, g))


data_table.sort(key=lambda tup: tup[1])

#Escribir la tabla en el archivo data

for index in data_table:
    data.write("%d %f %f %f %f\n" % index )
data.close()


#Analisis de PCA

data_transpose = numpy.array(data_table_pca).T

cov_matrix = numpy.cov(data_transpose)

#Vector propio

val_prop,vec_prop=linalg.eig(cov_matrix)

indices=numpy.argsort(val_prop)
val_prop.sort()

print val_prop
for i in indices:

    print vec_prop[i]



#Grafica de los valores medios de g en funcion de angulo

#Crea una lista para los angulos y otra para el promedio de g correspondiente

ang=[]
for angulo in data_table:
    ang.append(angulo[1])

ang = list(set(ang))
ang.sort()


means = []

for a in ang:
    sum = 0.0
    for angle in data_table:
        if (a == angle[1]):
           sum += angle[4]
    mean=sum/6.0
    means.append(mean)

#Grafica


xlabel('Angulo polar')
ylabel('Promedio de gravedad')
grid(True)
savefig('gravedad(angulo)')
plot(ang, means)
show()

F = []


#se crea F[] para almacenar el resutado
for i in range(len(means)):
    
	F.append(1-(means[i]/(9.81)))

sine = numpy.sin(numpy.array(ang)*numpy.pi/180)


ajuste_fluc = numpy.polyfit(sine,F,1.0)


xlabel('Angulo polar')
ylabel('F')
grid(True)
savefig('gravedad(angulo)')
plot(ang, F)
show()

Fp = []
rest = []

for j in range(len(sine)):

    Fp.append(sine[j] * ajuste_fluc[0])
    rest.append(Fp[j]-F[j])

xlabel('Angulo polar')
ylabel('Res')
grid(True)
savefig('gravedad(angulo)')
plot(ang, rest)
show()


