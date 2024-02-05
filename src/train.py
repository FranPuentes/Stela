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

if __name__ == "__main__":
   
   print(sys.argv);
   assert len(sys.argv) >= 3;
      
   origin=os.path.abspath(sys.argv[1]);
   target=os.path.abspath(sys.argv[2]);
   models=os.path.abspath(sys.argv[3]);
   
   assert os.path.isdir(origin);
   assert os.path.isdir(target);
   assert os.path.isdir(models);

   yaml_file = os.path.join(target,'dataset.yaml');
   basemodel = os.path.join(models,'yolov8x.pt');
   
   model = YOLO(task="detect", model=basemodel);

   model.train(imgsz=640, batch=32, epochs=200, data=yaml_file);
   
   metrics = model.val();
   print(metrics);

   model.export(format="onnx"  );
   model.export(format="engine");
