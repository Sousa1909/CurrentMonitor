#!/bin/bash

# Define ENV Variables
export FLASK_APP=shared/WebApp/run.py >> ~/.bashrc
export FLASK_ENV=development >> ~/.bashrc
export USE_NGROK=True >> ~/.bashrc
