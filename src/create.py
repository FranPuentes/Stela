#!/bin/env python3

import sys, os;
import json;

from pathlib import Path;

import cv2;
import numpy as np;
import math;

#-------------------------------------------------------------------------------
def rotate_xy(x, y, angulo, centro_x, centro_y):
    angulo_radianes = math.radians(angulo)
    
    x_centro = centro_x
    y_centro = centro_y
    
    x -= x_centro
    y = y_centro - y
    
    x_rotado = x * math.cos(angulo_radianes) - y * math.sin(angulo_radianes)
    y_rotado = x * math.sin(angulo_radianes) + y * math.cos(angulo_radianes)
    
    x_rotado += x_centro
    y_rotado  = y_centro - y_rotado
    
    return int(x_rotado), int(y_rotado)

#-------------------------------------------------------------------------------
def rotate_wh(w, h, angulo, centro_x, centro_y):
    return w, h;
    
#-------------------------------------------------------------------------------
def rotate_and_move(fnbase, target, dataset):
    assert os.path.isfile(f"{fnbase}.txt") and os.path.isfile(f"{fnbase}.PNG");
    assert type(target) is str and os.path.isdir(target);    
    
    basepath, filename = os.path.split(fnbase);
    
    #fnbase                                            basepath                             filename
    #/home/pcjf/Stela/data/obj_Train_data/frame_001080 /home/pcjf/Stela/data/obj_Train_data frame_001080
        
    imagen = cv2.imread(f"{fnbase}.PNG");
    alto, ancho, _ = imagen.shape;
    centro_x = ancho // 2;
    centro_y = alto  // 2;
    
    coords=[];
    with open(f"{fnbase}.txt") as fd:
         for line in fd:
             _, x, y, w, h = line.split();
             #x1=int((float(x)-float(w)/2)*ancho);
             #y1=int((float(y)-float(h)/2)*alto );
             #x2=int((float(x)+float(w)/2)*ancho);
             #y2=int((float(y)+float(h)/2)*alto );
             coords.append( (int(float(x)*ancho),int(float(y)*alto),int(float(w)*ancho),int(float(h)*alto)) );
    
    print(f"Rotando {fnbase}.PNG ", end='', flush=True);
    for angulo in range(0, 360, 10):
        matriz_rotacion = cv2.getRotationMatrix2D((centro_x, centro_y), angulo, 1);
        imagen_rotada = cv2.warpAffine(imagen, matriz_rotacion, (ancho, alto));
        
        imagen_dibujada=imagen_rotada;        
        for x,y,w,h in coords:
            xr, yr = rotate_xy(x, y, angulo, centro_x, centro_y);
            wr, hr = rotate_wh(w, h, angulo, centro_x, centro_y);
            imagen_dibujada = cv2.circle(imagen_dibujada, (xr, yr), 5, (0,0,255), thickness=-5)
            #imagen_dibujada = cv2.rectangle(imagen_dibujada, (x1, y1), (x2, y2), (0,0,255), 2);
            
        newname=f"{os.path.join(target,filename)}-{angulo:03}";
        cv2.imwrite(f"{newname}.png",imagen_dibujada);
        dataset.append( (f"{newname}.txt", f"{newname}.png") );
        print(".", end='', flush=True);
    print("", flush=True);
    exit(0);
    
#-------------------------------------------------------------------------------
def rotate_all(source, target):
    assert type(source) in (tuple, list) and len(source)==2 and all([(type(l) is list) for l in source]);
    assert type(target) is str and os.path.isdir(target);
    assert len(source[0]) == len(source[1]);
    
    txts=source[0];
    pngs=source[1];
 
    dataset=[];
    
    for i,txt_filename in enumerate(txts):
        fnbase, _ = os.path.splitext(txt_filename);
        rotate_and_move(fnbase, target, dataset);
        
    return dataset;    
        
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
   
   dataset=rotate_all(source=(txt_list,png_list), target=target);

   with open(os.path.join(target,"dataset.json"),"wt") as fd:   
        json.dump(dataset, fp=fd);
   
   