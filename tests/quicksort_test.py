# tests/quicksort_test.py
import sys
sys.path.append('../')  # Añade el directorio de la app al path, si es necesario

import numpy as np
import time
import matplotlib.pyplot as plt


from app.app import Product, quicksort_products  # Asegúrate de que estas clases y funciones estén disponibles en app.py

def generate_random_products(num):
    return [Product(i, "Producto" + str(i), "Descripción", "Categoría", np.random.randint(1, 100), np.random.uniform(0.99, 1000.99), "Fabricante", "Proveedor") for i in range(num)]

def test_quicksort_performance():
    sizes = [10, 100, 1000, 10000]
    times = []

    for size in sizes:
        products = generate_random_products(size)
        start_time = time.time()
        quicksort_products(products)
        times.append(time.time() - start_time)

    plt.plot(sizes, times, marker='o')
    plt.title("Rendimiento del Algoritmo Quicksort")
    plt.xlabel("Número de Productos")
    plt.ylabel("Tiempo en segundos")
    plt.yscale('log')  # Escala logarítmica para mejor visualización
    plt.xscale('log')  # Escala logarítmica para mejor visualización
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test_quicksort_performance()
