# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 13:26:09 2020

@author: medye
"""

import R1,R2,R3,R4,R5

def continuar(num):
    print("Script {} ejecutado".format(num))
    print("Pulse enter para continuar")
    input()
    
if __name__ == "__main__":
    R1.main()
    continuar('R1')
    R2.main()
    continuar('R2')
    R3.main()
    
    continuar('R3')
    R4.main()
    continuar('R4')
    R5.main()
    continuar('R5')