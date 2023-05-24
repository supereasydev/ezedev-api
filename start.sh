#!/bin/bash

cd /opt/ezedev-api
source /opt/ezedev-api/venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000