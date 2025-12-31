#!/bin/sh

PROMPT="$1"

# Ensure the credentials path is provided
if [ -z "$OBSIDIAN_GIT_CREDENTIALS_INPUT" ]; then
    echo "OBSIDIAN_GIT_CREDENTIALS_INPUT not set" >&2
    exit 1
fi

TEMP_FILE="$OBSIDIAN_GIT_CREDENTIALS_INPUT"

if [ -z "$TEMP_FILE" ]; then
# Ensure the credentials path is provided
if [ -z "$OBSIDIAN_GIT_CREDENTIALS_INPUT" ]; then
    echo "OBSIDIAN_GIT_CREDENTIALS_INPUT not set" >&2
    exit 1
fi

cleanup() {
    rm -f "$TEMP_FILE" "$TEMP_FILE.response"
}
trap cleanup EXIT

echo "$PROMPT" > "$TEMP_FILE"

TIMEOUT=30
START=$(date +%s)
while [ ! -e "$TEMP_FILE.response" ]; do
    if [ ! -e "$TEMP_FILE" ]; then
        echo "Trigger file got removed: Abort" >&2
        exit 1
    fi
    if [ $(($(date +%s) - START)) -ge "$TIMEOUT" ]; then
        echo "Timeout waiting for response" >&2
        exit 1
    fi
    sleep 1
    if [ $(($(date +%s) - START)) -ge $TIMEOUT ]; then
        echo "Timeout waiting for response" >&2
        exit 1
    fi
    sleep 0.1
done

RESPONSE=$(cat "$TEMP_FILE.response")

echo "$RESPONSE"
