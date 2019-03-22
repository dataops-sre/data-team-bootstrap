#!/bin/sh
set -e

/opt/datadog-agent/bin/agent/agent health
python container_memory_check.py