# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 00:01:32 2020

@author: karen
"""

from cx_Freeze import setup, Executable

setup( name = 'ventana', version = '0.1',
      description= 'ventana', 
      executables = [Executable('dump_to_gr.py')])