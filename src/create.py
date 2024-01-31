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
    
    x_centro = centro_x;
    y_centro = centro_y;
    
    x -= x_centro;
    y  = y_centro - y;
    
    x_rotado = x * math.cos(angulo_radianes) - y * math.sin(angulo_radianes);
    y_rotado = x * math.sin(angulo_radianes) + y * math.cos(angulo_radianes);
    
    x_rotado += x_centro;
    y_rotado  = y_centro - y_rotado;
    
    return int(x_rotado), int(y_rotado);
    
#-------------------------------------------------------------------------------
def rotate_wh(w, h, angulo):
    g_rad = math.radians(angulo);

    w_prime = abs(w*math.cos(g_rad)) + abs(h*math.sin(g_rad));
    h_prime = abs(w*math.sin(g_rad)) + abs(h*math.cos(g_rad));

    return int(w_prime), int(h_prime);

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
             c, x, y, w, h = line.split();
             coords.append( (c, int(float(x)*ancho),int(float(y)*alto),int(float(w)*ancho),int(float(h)*alto)) );
    
    print(f"Rotando {fnbase}.PNG ", end='', flush=True);
    for angulo in range(0, 360, 5):
        matriz_rotacion = cv2.getRotationMatrix2D((centro_x, centro_y), angulo, 1);
        imagen_rotada = cv2.warpAffine(imagen, matriz_rotacion, (ancho, alto));
        
        new_coords=[];
        imagen_dibujada=imagen_rotada;
        for c,x,y,w,h in coords:
            xr, yr = rotate_xy(x, y, angulo, centro_x, centro_y);
            wr, hr = rotate_wh(w, h, angulo);
            x1=(xr-wr//2);
            x2=(xr+wr//2);
            y1=(yr-hr//2);
            y2=(yr+hr//2);
            
            x1=max(x1,0);
            x1=min(x1,ancho-1);
            
            y1=max(y1,0);
            y1=min(y1,alto-1);
            
            x2=max(x2,0);
            x2=min(x2,ancho-1);
            
            y2=max(y2,0);
            y2=min(y2,alto-1);
            
            if (x2-x1)*(y2-y1) < (w*h)*0.6: continue;
            
            #imagen_dibujada = cv2.circle   (imagen_dibujada, (xr, yr), 5, (0,0,255), thickness=-5)
            #imagen_dibujada = cv2.rectangle(imagen_dibujada, (x1,y1), (x2,y2), (0,0,255), 2);
            new_coords.append( (c, x1+(x2-x1+1)//2, y1+(y2-y1)//2, x2-x1+1, y2-y1+1) );
            
        newname=f"{os.path.join(target,filename)}-{angulo:03}";
        with open(f"{newname}.txt","wt") as fd:
             for c in new_coords:
                 print(f"{c[0]} {c[1]/ancho} {c[2]/alto} {c[3]/ancho} {c[4]/alto}", file=fd);
        cv2.imwrite(f"{newname}.png",imagen_dibujada);
        dataset.append( (f"{newname}.txt", f"{newname}.png") );
        print(".", end='', flush=True);
    print("", flush=True);
    
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
        #if i>=10: break;
        
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
   
   