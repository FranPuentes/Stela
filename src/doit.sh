#!/bin/bash

# TODO hacer logs
# TODO mandar notificaciones

DATA="../data/obj_Train_data"
TEMP="../tmp"
MODELS="../models"

mkdir -p "${TEMP}"
mkdir -p "${MODELS}"

#./create.py "${DATA}" "${TEMP}" "${MODELS}" 
./tune.py   "${DATA}" "${TEMP}" "${MODELS}"
#./train.py  "${DATA}" "${TEMP}" "${MODELS}"
#./test.py   "${DATA}" "${TEMP}" "${MODELS}"
