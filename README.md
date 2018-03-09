# Markov-Chain-Music-Production
Python Music Production Program - An extremely simplified and re factored program based loosely on the Markov-Based element of my masters thesis. A lot simpler in nature and complexity compared to my thesis work. Despite this it produces some interesting results.
The lack of complexity is based on the program limiting generation to a single instrument whilst also limiting the musical octave.

Requirements:

Python3
Mido
Numpy
Pandas

Usage:
Simply place midi files into the /midi/ folder and then run the Markov.py file in your chosen IDE or via the python command in the console. The program will then output a generated sequence into the /outputs/ folder.
The name of the output will be printed in the python console.

The /outputs/ folder contains a number of examples generated solely using the midi for Fur Elise. For varied results, it is better to use more than a single midi as this will allow the program to create a better generalisation.