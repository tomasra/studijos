#!/bin/sh
PYTHONPATH="${PYTHONPATH}":/scratch/lustre/home/tora6799/python/
export PYTHONPATH

mpiexec -n 4 python run_pcalc.py

