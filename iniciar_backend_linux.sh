#!/bin/bash
cd Backend
source ../.venv/bin/activate
uvicorn main:app --reload