"""
Práctica 3: Sistema musculoesquelético.

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Gustavo Ortega Odabachea
Número de control: 23212223
Correo institucional: L23212223@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

#Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N = round(tend/dt) + 1
t = np.linspace(t0,tend,N)
F = np.zeros(N); F[round(1/dt):round(2/dt)] = 1


# Circuitos eléctricos para control y caso: [α, Cs, Cp, R]
params_circuito = {
    'Control': [0.25, 10E-6, 100E-6, 100],
    'Caso': [0.25, 10E-6, 100E-6, 10E3]
}

def sistema(alpha, Cs, Cp, R):
    num = [Cs*R, 1-alpha]
    den =[R*(Cp+Cs),1]
    L = np.roots(den)
    sys = ctrl.tf(num,den)
    return sys, L

Control, L_control = sistema(*params_circuito['Control'])
Caso, L_caso = sistema(*params_circuito['Caso'])

print(f"Polo Control: L = {L_control[0]:.3e}\n")
print(f"Polo Caso: L = {L_caso[0]:.3e}\n")

# Componentes del controlador PI para el caso
kP, kI = 0.217, 3665.036
Cr = 1E-6
Re = 1/(Cr*kI) 
Rr = kP*Re
numPID = [Rr*Cr, 1]
denPID = [Re*Cr, 0]
PID = ctrl.tf(numPID,denPID)
print(f"El valor de la resistencia Rr es de {Rr} Ohms.\n")
print(f"El valor de la resistencia Re es de {Re} Ohms.\n")
print(f"Función de transferencia del controlador PID: {PID}\n")

# Sistema de control en lazo cerrado para el caso
PI = ctrl.feedback(ctrl.series(PID, Caso), 1, sign = -1)
print(f"Función de transferencia del sistema de control en lazo cerrado: {PI}")

_, Fsx = ctrl.forced_response(Control, t, F, x0)
_, Fsy = ctrl.forced_response(Caso, t, F, x0)
_, Tratamiento = ctrl.forced_response(PI, t, Fsx, x0)

#Colores
clr1 = np.array([9,21,64])/255
clr2 = np.array([27,94,32])/255
clr3 = np.array([246,36,64])/255
clr4 = np.array([245, 153, 198])/255

#Respuestas: Simulaciones numéricas
fg = plt.figure(1)
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,F,'-',color=clr1,label='F(t)')
plt.plot(t,Fsx,'-',color=clr2,label='Fs(t): Control')
plt.plot(t,Fsy,'--',color=clr3,label='Fs(t): Caso')
plt.plot(t,Tratamiento,':',color=clr4,label='PID(t): Tratamiento')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1);plt.yticks(np.arange(-0.1,1.2,0.1))
plt.xlabel('t [s]')
plt.ylabel('Fi(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=4,frameon=False)
plt.show()
fg.savefig('Señal_python.pdf',bbox_inches='tight')