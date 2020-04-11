
#!/bin/bash

# wget https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip

# unzip chromedriver_linux64.zip

# cp chromedriver /usr/local/bin

BUILD_DIR=${1:-}
CACHE_DIR=${2:-}
ENV_DIR=${3:-}

BIN_DIR=$BUILD_DIR/.chromedriver/bin
mkdir -p $BIN_DIR


wget  https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip
unzip -o chromedriver_linux64.zip -d $BIN_DIR
unzip chromedriver_linux64.zip 