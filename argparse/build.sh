#!/bin/bash
source venv3.10-linux-arm64/bin/activate
pyinstaller --name exec-test --onefile main.py
pyinstaller exec-test.spec
cp dist/exec-test ./