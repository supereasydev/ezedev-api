#!/bin/bash

cd /opt/backend
source /opt/backend/venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000