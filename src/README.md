# Código fuente de **Stela**

Acciones (*TODO list*):

* Crear los datasets (train y test) a partir de las imágenes etiquetadas (*create.py*).

* Preprocesar las imágenes si es posible: generar las diferencias entre frames para tener dos datasets (const y diff) (*preprocess.py*).

* Para cada imagen **con** etiquetas: generar al menos 36 variaciones rotando las imágenes y sus etiquetas, en giros de 10 grados (*variations.py*).

* Cada dataset se almacena en "../tmp": "../tmp/const" y "../tmp/diff" (*dump.py*).

* Entrenar cada dataset por separado, evaluar por separado (*train.py* y *evaluate.py*).

Todos estos procesos deberán ejecutarse automáticamente.



