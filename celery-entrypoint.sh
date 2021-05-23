#!/bin/bash
celery -A elephant worker -l info -Q others -n others@%h
