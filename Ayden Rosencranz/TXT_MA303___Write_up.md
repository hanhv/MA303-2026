Project: Eulers Method Solver (Eulers, Improved Eulers, and Runge-Kutta)
*---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---*

Project objective: TO create a program that was capable of answering hws: 2.4, 2.5, & 2.6, this also helped me better
understand the application of the math and how to best utilize these equations to solve problems.

*---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---*

Disclosures: The uselization of AI was used in the creation of some sections, parts, lines of code. This was allowed by my teacher and was used in a way that allowed me to best practice
the math more so than my ability to code. The model utilized was Claude by Anthropic.

*---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---*
CODE OVER VEIW and OPPERATION
-----------------------------

### Imports Section ###
The import ection is utilized to import nessacary funtions and opperations required to computate each varriation of the eulers method.
The Imports utilized in final verison: Math (Math Library).
The Imports utilized in ealier itterations: import numpy as np, import ast, import operator as op, import math.

### Get user function section ###
The get user function section is a nessacary step that uses math libraries to create a stored data set allowing the code to be more flexiable. This allows the user to input and slove for more complex equations such as X^2+Y^2 which would be transposed and stored as X**2+Y**2. This gives both the user a more intuitive and flexible solver program. This section also has a secondary component that will also work for expressions or more complex elements such as sine and cosine functions or exponentials.

### Method solving section ###
This section