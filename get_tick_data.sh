#!/bin/bash

CURRENT_DATE=$(date +%Y%m%d)
echo "Current Date:${CURRENT_DATE}"

TARGET_SCRIPT=$1

echo "Target Script: ${TARGET_SCRIPT}"

source activate option_data_processor

LOG_FILE="./logs/tick_data_${CURRENT_DATE}.log"

nohup python -u  "${TARGET_SCRIPT}" > "${LOG_FILE}" 2>&1 &
echo "Saved to log file: ${LOG_FILE}"

conda deactivate

