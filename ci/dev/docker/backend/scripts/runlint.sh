#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=crm.settings
pylint --rcfile=.pylintrc `ls`
