#!/bin/env python3

import sys, os;
import json;
import shutil;

from pathlib import Path;

import cv2;
import numpy as np;
import math;
import random;

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
   
   with open(os.path.join(target,"dataset.json"),"rt") as fd:
        dataset=json.load(fp=fd);

   trainset=[];
   testset =[];
   
   if not os.path.isfile(os.path.join(target,"trainset.json")) or not os.path.isfile(os.path.join(target,"testset.json")):
      trainset, testset = split_list(dataset, 90);
      with open(os.path.join(target,"trainset.json"),"wt") as fd:
           json.dump(trainset,fp=fd);
      with open(os.path.join(target,"testset.json"),"wt") as fd:
           json.dump(testset,fp=fd);
      
   else:
      with open(os.path.join(target,"trainset.json"),"rt") as fd:
           trainset=json.load(fp=fd);
      with open(os.path.join(target,"testset.json"),"rt") as fd:
           testset=json.load(fp=fd);
   
   for item in trainset:

       txt=item[0];
       path, filename = os.path.split(txt);
       shutil.move(txt, os.path.join(path,"train",filename));

       png=item[1];
       path, filename = os.path.split(png);
       shutil.move(png, os.path.join(path,"train",filename));
       
   for item in testset:

       txt=item[0];
       path, filename = os.path.split(txt);
       shutil.move(txt, os.path.join(path,"test",filename));

       png=item[1];
       path, filename = os.path.split(png);
       shutil.move(png, os.path.join(path,"test",filename));
