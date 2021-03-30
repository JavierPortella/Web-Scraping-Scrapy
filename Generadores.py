
# Función de un generador
def my_gen():

    # Definimos una variable
    a = 1

    #Permite recordar el estado de dónde se quedó la función.
    yield a

    a= 2
    yield a

    a = 3
    yield a

# Guardar el generador en una variable
my_first_gen = my_gen()

# Next llama a la función y usa el estado de dónde se quedó la función
print(next(my_first_gen))
print(next(my_first_gen))
print(next(my_first_gen))