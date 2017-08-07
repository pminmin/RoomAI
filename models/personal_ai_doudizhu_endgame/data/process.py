#!/bin/python
f = open("4_give_hand.txt")
f1 = open("4.txt","w")
for line in f:
    f1.write(line.strip()[2:len(line)] + "\n")
