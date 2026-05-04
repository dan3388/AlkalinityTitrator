#!/usr/bin/env bash
pipenv sync -d
pipenv run pytest -vv
