Código fuente de **Stela**

Acciones:

> Crear los datasets (train y test) a partir de las imágenes etiquetadas.

> Preprocesar las imágenes si es posible: generar las diferencias entre
> frames para tener dos datasets (const y diff).

> Para cada imagen **con** etiquetas: generar al menos 36 variaciones
> rotando las imágenes y sus etiquetas, en giros de 10 grados.

> Cada dataset se almacena en "../tmp": "../tmp/const" y "../tmp/diff".

> Entrenar cada dataset por separado, evaluar por separado.


Todos estos procesos deberán ejecutarse automáticamente.



