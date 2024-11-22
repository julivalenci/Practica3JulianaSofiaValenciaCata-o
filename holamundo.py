import tkinter as tk   #interfaces graficas
from tkinter import ttk  #interfaces graficas
from nltk import CFG   # definir gramatica libre de contexto
from nltk.tree import Tree  #generar el arbol
from nltk.parse.chart import ChartParser  #analizador sintatico para gramatica libre de contexto

# definicion de las expresiones matematicas  de la gramatica libre de contexto
grammar = CFG.fromstring("""
    E -> E '+' T | E '-' T | T
    T -> T '*' F | F
    F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'x' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
""")

# esta funcion toma la oracion ingresada por el usuario y separa los operadores, parentesis y signos para poder ser procesados correctamente por el parser
# genera el arbol
def generate_derivation_steps(grammar, sentence):
    parser = ChartParser(grammar)
    try:
        #lista con los posibles arboles generados
        trees = list(parser.parse(sentence.split())) #tokrtiniza la expresion ingresada
        if len(trees) > 0:
            tree = trees[0]  # Tomamos el primer árbol generado
            steps = []


        # funcion para recorrer el arbol y registrarlo en una lista llamada steps
        
            def traverse_tree(tree, steps):
                if isinstance(tree, Tree):
                    if len(tree) > 1:  # Si no es terminal, añadir el paso
                        # cadena que representa los pasos de derivación
                        step = f"{tree.label()} -> {' '.join(child.label() if isinstance(child, Tree) else child for child in tree)}"
                        steps.append(step)  # agrega la cadena a la lista steps
                    for child in tree:
                        traverse_tree(child, steps)


            traverse_tree(tree, steps)
            # Devolver los pasos y el árbol
            return steps, tree  
        else:
            return ["No se pudo derivar la oración "], None
    except ValueError:
        return ["No se pudo derivar la oración"], None




#funciones para mostrar en los paneles de texto

# Función para abrir una nueva ventana con los pasos y el arbol
# muestra el arbol a partir de la estructura de derivación
def open_steps_and_tree_window(steps, tree):
    steps_window = tk.Toplevel(window)  # crea una ventana secundaria
    steps_window.title("Pasos de Derivación y Árbol")
    steps_window.geometry("600x400")


    # Panel de texto para los pasos
    steps_text = tk.Text(steps_window, wrap="word", bg="white", relief="solid", width=40)
    steps_text.insert("1.0", "\n".join(steps))
    steps_text.configure(state="disabled") 
    steps_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Mostrar el árbol en un canvas
    if tree:
        tree_canvas = tk.Canvas(steps_window, bg="white", relief="solid")
        tree_canvas.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        tree.draw()  #  abre una ventana separada con el árbol usando NLTK



# Función para procesar la derivación y mostrar los pasos y el árbol
# toma la entrada del usuario desde el cuadro de texto
def process_derivation():
    sentence = input_box.get().strip()
    if not sentence:
        result_label.config(text="Por favor, ingresa una oracion.")
        return

    steps, tree = generate_derivation_steps(grammar, sentence) # llama a generate derivation para generar pasos de derivacion
    if tree:
        result_label.config(text="arbol y derivacion generados correctamente.") # generacion exitosa
        open_steps_and_tree_window(steps, tree)
    else:
        result_label.config(text="No se pudo generar la derivación.") # error al generar





#interfacez

# Interfaz gráfica principal
window = tk.Tk()
window.title("arbol sintatico")
window.geometry("500x100")

# Mostrar la gramática
grammar_label = tk.Label(window, text="Gramatica definida:\n" + str(grammar), justify="left", anchor="w")
grammar_label.pack(pady=10)

# Entrada para la oración
input_label = tk.Label(window, text="Ingresa la oración:")
input_label.pack()
input_box = tk.Entry(window, width=40)
input_box.pack()

# Opciones de derivación
var = tk.StringVar(value="Izquierda")
ttk.Radiobutton(window, text="Derivacion por la Izquierda", variable=var, value="Izquierda").pack()
ttk.Radiobutton(window, text="Derivacion por la Derecha", variable=var, value="Derecha").pack()

# Botón para generar la derivación
btn_generate_derivation = tk.Button(window, text="Generar derivación y arbol", command=process_derivation)
btn_generate_derivation.pack(pady=10)

# Mensaje de resultados
result_label = tk.Label(window, text="", fg="blue")
result_label.pack(pady=10)

# Inicia la ventana principal
window.mainloop()
