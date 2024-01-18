#!/bin/bash

# TODO hacer logs
# TODO mandar notificaciones

TEMP="../tmp"

(./create_datasets.py   && \
 ./preprocess.py        && \
 ./variations.py        && \
 ./dump_datasets.py     && \
 ./train_datasets.py    && \
./evaluate_datasets.py) > ${TEMP}/out.log 2> ${TEMP}/err.log


