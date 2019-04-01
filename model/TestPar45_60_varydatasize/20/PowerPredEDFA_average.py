# coding: utf-8

# In[171]:

# Ido Michael
import tensorflow as tf
import os, struct
import numpy as np
import matplotlib.pyplot as plt
import ParsePowerEDFA
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import math
import sys
import configparser
import random


print(tf.__version__)
# In case we need to average results of 5 different debug files and plot them on a graph.
# ParsePowerEDFA.getTestFiles()

# Average files by name and then write collected results into a csv file.
[testdb, testmse, testmae, tr2, tr4, tr6, tr8, tr1, mse_tr, mae_tr] = ParsePowerEDFA.averageResults("TestPar45_60_20")
[val2, val4, val6, val8, val1, mse_val, mae_val] = ParsePowerEDFA.averageResults_val("TestPar45_60_20")
ParsePowerEDFA.plot_to_matrix(tr2, tr4, tr6, tr8, tr1, mse_tr, mae_tr)
ParsePowerEDFA.plot_to_matrix_Val(val2, val4, val6, val8, val1, mse_val, mae_val)
ParsePowerEDFA.plot_to_matrix_test(testdb, testmse, testmae)
# 20%
# [testdb, val2, val4, val6, val8, val1] = ParsePowerEDFA.averageResults([
#     "./TestPar29.ini140-debug.log",
#     "./TestPar29.ini84-debug.log",
#     "./TestPar29.ini150-debug.log"
# ])

# [testdb, val2, val4, val6, val8, val1] = ParsePowerEDFA.averageResults(["./test/TestPar25.ini-smaller53-debug.log", "./test/TestPar25.ini-smaller103-debug.log", "./test/TestPar25.ini-smaller25-debug.log", "./test/TestPar25.ini-smaller37-debug.log", "./test/TestPar25.ini-smaller30-debug.log"])
# ParsePowerEDFA.plotGraph(val2, val4, val6, val8, val1)

