
my_list = [1,2,3,4,5]

# Para recorrer una lista normalmente se usa un for para recorrer la lista
# En este ejemplo se verá qué hace Python al hacer el recorrido

my_iter = iter(my_list)

print(type(my_iter))
# <class 'list_iterator'>


#Extraer los elementos
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))

#Al rebasar la cantidad de elementos que contenía la lista, genera un error
print(next(my_iter))