#!/usr/bin/env bash
source .venv/bin/activate
flask --debug --app main run
deactivate
