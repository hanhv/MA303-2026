This code first imports laplace and inverse laplace transforms from the sympy python library.
It then creates 2 variables those being t and s using the sympy library. After this it ensures that the variables are greater than 0.
Then we define the variable compute_laplace, we ask for the user to import their function and then recall our local variables of t and s.
We then check if the function includes the correct variable and if it does it passes but if it doesn't then an error is sent and you are reprompted to put in a different function.
Once your function passes the variable check it then is transformed using the laplace_transform function from the sympy library.
after it is transformed it is outputted back to you and you are reprompted on what you want to do next.
Next in the code is the inverse laplace transform calculation section. 
It starts out the same as the regular laplace transform section of code up until the variable pass line. 
After your variables are correct then it checks to see if you have a rational transfer function, it does this by making sure that the variable in the numerator has a lower order than the denominator. It does this because a transfer function can not have a higher order in the numerator. 
Once your transfer function passes this check point then the inverse_laplace_transform function is applied and outputs the final inversed transform and then reprompts you on what you want to do next.
The final section of code is the input section, it first gives you 3 options those being, laplace transform, inverse laplace transform, and end the code.
If you choose option 1 it prompts you to enter the function you want to do the transform on and then does the laplace transform. 
If you choose option 2 it prompts you to enter the transform you want to do the inverse transform on and then does the inverse laplace. 
If you choose option 3 it just ends the code and if you want to use it again you have to restart the code.
