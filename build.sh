#!/bin/bash

# 告诉脚本如果任何命令失败，则立即退出
set -e

echo "--- Installing system dependencies for Pillow ---"

# 使用 yum 安装 Pillow 编译时所需的开发库
# 我们安装了一系列常见的图像格式支持库
yum install -y \
  libjpeg-turbo-devel \
  zlib-devel \
  libtiff-devel \
  freetype-devel \
  lcms2-devel \
  libwebp-devel \
  tcl-devel \
  tk-devel \
  harfbuzz-devel \
  fribidi-devel \
  libraqm-devel \
  libimagequant-devel \
  libxcb-devel

echo "--- System dependencies installed. Installing Python packages. ---"

# 继续执行常规的 pip 安装
pip install -r requirements.txt

echo "--- Build script finished. ---"