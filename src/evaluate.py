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

   model_name = "../runs/detect/train/weights/best.pt";

   metrics = YOLO(model_name).val();
   
   print("="*80);
   print("map50-95");
   print("="*80);
   print(metrics.box.map);
   
   print("="*80);
   print("map50");
   print("="*80);
   print(metrics.box.map50);
   
   print("="*80);
   print("map75");
   print("="*80);
   print(metrics.box.map75);
   
   print("="*80);
   print("maps");
   print("="*80);
   print(metrics.box.maps);

   