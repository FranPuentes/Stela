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

   model.tune(data=yaml_file, epochs=30, iterations=300, optimizer='AdamW', plots=False, save=False, val=False);

