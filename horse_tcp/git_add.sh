#!/bin/bash
git add components/ main/ CMakeLists.txt  log.txt Makefile README.md sdkconfig
git commit -m $1
git push
