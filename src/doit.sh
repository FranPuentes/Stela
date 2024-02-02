#!/bin/bash

# TODO hacer logs
# TODO mandar notificaciones

DATA="../data/obj_Train_data"
TEMP="../tmp"
MODELS="../models"

mkdir -p "${TEMP}"
mkdir -p "${MODELS}"

#./create.py      "${DATA}" "${TEMP}" "${MODELS}" 
./train.py       "${DATA}" "${TEMP}" "${MODELS}"
#./evaluate.py    "${DATA}" "${TEMP}" "${MODELS}"
