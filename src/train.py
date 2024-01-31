#!/bin/env python3

import sys, os;
import json;
import shutil;

from pathlib import Path;

import cv2;
import numpy as np;
import math;
import random;

from ultralytics import YOLO;

def split_list(lista, porcentaje):
    tamaño = len(lista);
    tamaño_parte = int(tamaño * porcentaje / 100);
    parte_aleatoria = random.sample(lista, tamaño_parte);
    resto = [elemento for elemento in lista if elemento not in parte_aleatoria];
    return parte_aleatoria, resto;

if __name__ == "__main__":
   
   assert len(sys.argv) >= 3;
      
   origin=os.path.abspath(sys.argv[1]);
   target=os.path.abspath(sys.argv[2]);
   models=os.path.abspath(sys.argv[3]);
   
   assert os.path.isdir(origin);
   assert os.path.isdir(target);
   assert os.path.isdir(models);

   yaml_file = os.path.join(target,'dataset.yaml');
   basemodel = 'yolov8n.pt';
   
   model = YOLO(task="detect").load(basemodel);

   model.train(imgsz=640, batch=16, epochs=100, data=yaml_file);
   
   metrics = model.val();
   print(metrics);

   model.export(format="onnx"  );
   model.export(format="engine");
   
   #model.save(os.path.join(models,'stela.pt'));

   