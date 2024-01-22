#!/bin/env python3

import sys, os;

from pathlib import Path;

import cv2;
import numpy as np;
import math;

#-------------------------------------------------------------------------------
def rotate_and_move(fnbase, target):
    assert os.path.isfile(f"{fnbase}.txt") and os.path.isfile(f"{fnbase}.PNG");
    assert type(target) is str and os.path.isdir(target);
    
    imagen = cv2.imread(f"{fnbase}.PNG");
    alto, ancho, _ = imagen.shape;
    centro_x = ancho // 2;
    centro_y = alto  // 2;
    
    print(f"Rotando {fnbase}.PNG ", end='', flush=True);
    for angulo in range(0, 360, 10):        
        matriz_rotacion = cv2.getRotationMatrix2D((centro_x, centro_y), angulo, 1);
        imagen_rotada = cv2.warpAffine(imagen, matriz_rotacion, (ancho, alto));
        cv2.imwrite(f"{fnbase}-{angulo:03}.png",imagen_rotada);
        print(".", end='', flush=True);
    print("", flush=True);
    
#-------------------------------------------------------------------------------
def rotate_all(source, target):
    assert type(source) in (tuple, list) and len(source)==2 and all([(type(l) is list) for l in source]);
    assert type(target) is str and os.path.isdir(target);
    assert len(source[0]) == len(source[1]);
    
    txts=source[0];
    pngs=source[1];
    
    for i,txt_filename in enumerate(txts):
        fnbase, _ = os.path.splitext(txt_filename);
        rotate_and_move(fnbase, target);
        
################################################################################
if __name__ == "__main__":
   
   assert len(sys.argv) >= 3;
      
   origin=os.path.abspath(sys.argv[1]);
   target=os.path.abspath(sys.argv[2]);
   
   assert os.path.isdir(origin);
   assert os.path.isdir(target);
   
   source = Path(origin);
   txt_list = list(source.glob("*.txt"));
   png_list = [];
   
   txt_list=[fn for fn in txt_list if os.path.getsize(fn)>0];
   
   for txt_filename in txt_list:
       base, ext = os.path.splitext(txt_filename);
       assert ext==".txt";
       png_filename=f"{base}.PNG";
       assert os.path.isfile(png_filename);
       png_list.append(png_filename);
       assert png_list.index(png_filename)==txt_list.index(txt_filename);
   
   print(target)
   #rotate_all(source=(txt_list,png_list), target=target);
   