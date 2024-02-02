# Código fuente de **Stela**

Acciones (*TODO list*):

* Crear los datasets (train y test) a partir de las imágenes etiquetadas (*create.py*).

* Preprocesar las imágenes si es posible: generar las diferencias entre frames para tener dos datasets (*no se hace*).

* Para cada imagen con etiquetas: generar al menos 72 variaciones rotando las imágenes y sus etiquetas, en giros de 5 grados (*create.py*).

* Cada dataset se almacena en "../tmp/train" (95%) y "../tmp/test" (5%) (*create.py*).

* Entrenar el trainset y evaluar con testset (*train.py* y *evaluate.py*,respectivamente).

Todos estos procesos se ejecutan en background.
