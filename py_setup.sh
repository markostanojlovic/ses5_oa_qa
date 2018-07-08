#!/bin/bash
set -x
python36 -m venv VENV
source VENV/bin/activate
python -m pip install --upgrade pip
python -m pip install -r python_requirement.txt
set +x
