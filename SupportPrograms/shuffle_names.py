#!/usr/bin/env python
# coding: utf-8
# Randomly shuffle names to see who starts by chance
# Regards, Sam.
#------------------------------------------------------------


import random

names = ["Motoki","Daisuke","Sato"]

random.shuffle(names,random.random)
print(names)
