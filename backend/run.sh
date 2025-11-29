#! /usr/bin/env bash
set -e
python3 backend_pre_start.py;
sleep 10;
alembic upgrade head;
python3 main.py;