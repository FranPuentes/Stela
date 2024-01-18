#!/bin/bash

# TODO hacer logs
# TODO mandar notificaciones

DATA="../data"
TEMP="../tmp"

mkdir -p "${TEMP}"

(./create.py      "${DATA}" "${TEMP}" && \
 ./preprocess.py  "${DATA}" "${TEMP}" && \
 ./variations.py  "${DATA}" "${TEMP}" && \
 ./dump.py        "${DATA}" "${TEMP}" && \
 ./train.py       "${DATA}" "${TEMP}" && \
 ./evaluate.py    "${DATA}" "${TEMP}"    ) > "${TEMP}/out.log" 2> "${TEMP}/err.log"


