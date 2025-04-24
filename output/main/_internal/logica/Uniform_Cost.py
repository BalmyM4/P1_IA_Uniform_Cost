import networkx as nx

# Función auxiliar para registrar el paso a paso del algoritmo
def paso_paso_str(nivel: int, cola: list, paso_paso: str, nodo_actual: str):
    paso_paso += f"{nivel}"  # Nivel actual del algoritmo (cuántas iteraciones van)
    
    for tupla in enumerate(cola):
        # Solo mostramos los primeros 3 caracteres del nombre del nodo
        camino_str = [nodo[:3] for nodo in tupla[1][2]]
        camino_str = " -> ".join(camino_str)

        paso_paso += f"\t{tupla[1][0]}"  # Costo acumulado
        paso_paso += f"\t{nodo_actual[:3]}" if tupla[0] == 0 and nodo_actual is not None else "\t"
        paso_paso += f"\t{camino_str} «\n" if tupla[0] == 0 else f"\t{camino_str}\n"
    
    paso_paso += "\n"
    return paso_paso


# Implementación del algoritmo Uniform Cost Search sin usar heapq
def uniform_cost_search(grafo: nx.Graph, inicio: str, objetivo: str):
    
    paso_paso = ""     # Para guardar el detalle de cada iteración
    
    nivel = 0          # Contador de pasos o iteraciones
    
    cola = []          # Cola para almacenar el paso a paso
    
    visitados = []     # Para no volver a visitar nodos
    
    nodo_actual = None # Nodo que se está procesando en esta iteración
    
    cola.append((0, inicio, [inicio]))  # Inicializar la cola con el nodo de inicio
    
    # Mientras haya nodos en la cola
    while cola:
        
        # Ordenar la cola por el menor costo acumulado (prioridad)
        cola.sort(key=lambda x: x[0])

        # Registrar el estado actual de la cola
        paso_paso = paso_paso_str(nivel, cola, paso_paso, nodo_actual)

        # Extraer el nodo con menor costo
        costo_actual, nodo_actual, camino = cola.pop(0)

        # Si es el objetivo, terminamos
        if nodo_actual == objetivo:
            return camino, costo_actual, paso_paso

        # Evitar re-visitar nodos
        if nodo_actual in visitados:
            continue
        
        visitados.append(nodo_actual)  # Registrar nodo como visitado

        # Explorar vecinos
        for vecino in grafo.neighbors(nodo_actual):
            if vecino not in visitados:
                
                # Obtener el peso de la arista desde el grafo de networkx
                peso = grafo[nodo_actual][vecino]['weight']
                
                # Agregar nuevo camino a la cola
                cola.append((costo_actual + peso, vecino, camino + [vecino]))
        
        nivel += 1  # Avanzar al siguiente nivel de búsqueda

    # Si no se encuentra camino
    return None, -1, "No se encontró camino"
