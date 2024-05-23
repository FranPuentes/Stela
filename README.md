# Stela

Herramientas para el entrenamiento de modelos para la detección de estelas en imágenes del firmamento.

<img src="https://github.com/FranPuentes/Stela/assets/2001456/e475352e-1518-47c1-bacb-df6c87123de1" width="300" height="200">

---
**Vídeo de la noche del 13 al 14 de febrero del 2024**

https://github.com/FranPuentes/Stela/assets/2001456/372dd0f2-eb4d-45fb-8679-da2225178a96

**Vídeo procesado con un *theshold* del 0.40**

https://github.com/FranPuentes/Stela/assets/2001456/2cc84c51-a4fe-4ecc-bd71-8511407df52e

**Para probar el modelo usando _gradio_**

```python
import os, cv2, gradio;

TRACKING=True;
BASE="."; # donde esté situado el modelo
model_path="best.pt";

def detect_onvideo(filename):
    import PIL;
    from ultralytics import YOLO;

    model = YOLO(model_path);

    assert os.path.isfile(filename), f"El archivo '{filename}' no existe";
    cap = cv2.VideoCapture(filename);
    try:
      assert cap.isOpened(), f"Error al abrir el archivo de video: {filename}";

      frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));
      frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT));
      fps = cap.get(cv2.CAP_PROP_FPS);
      codec_in = int(cap.get(cv2.CAP_PROP_FOURCC));
      codec_out = ''.join([chr((codec_in >> 8 * i) & 0xFF) for i in range(4)]);

      tempname=os.path.join(BASE,"temp_video.avi");

      out = cv2.VideoWriter(tempname, cv2.VideoWriter_fourcc(*"XVID"), fps//2, (frame_width, frame_height), True);
      try:
        ok, frame = cap.read();
        while ok:

              if not TRACKING: results = model(frame, stream=False, verbose=False, conf=0.40);
              else:            results = model.track(frame, persist=True, verbose=False, conf=0.40);

              annotated_frame = results[0].plot();
              out.write(annotated_frame);

              ok, frame = cap.read();
      finally:
        out.release();

      return tempname;

    finally:
      cap.release();

intf = gradio.Interface(fn=detect_onvideo, inputs="video", outputs="video");
intf.launch(debug=True)
```


