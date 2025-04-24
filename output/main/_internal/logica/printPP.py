
def decorador():
    print("")
    print("="*100)
    print("")

def printPP( camino: str, costo: float, paso_paso: str ):
    
    decorador()
    
    print("Nivel\t\tCosto\t\tNodos Visitados\t\tCamino")
    
    print(paso_paso)
   
    decorador()
    
    print(f"Ruta: {camino}")
    print(f"Costo: {costo}")
    
    decorador()