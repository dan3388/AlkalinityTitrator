#!/usr/bin/env bash
pipenv sync -d
pipenv run python main.py -gui
