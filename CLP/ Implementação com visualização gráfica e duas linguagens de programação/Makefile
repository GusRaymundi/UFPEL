# Makefile
# Constrói a biblioteca C e executa a interface Python.
# Alvos principais:
#   make all    -> compila a biblioteca compartilhada (mandelbrot.so/.dll/.dylib)
#   make run    -> executa a GUI Python
#   make clean  -> remove artefatos de build

CC      ?= gcc
CFLAGS  ?= -O2 -fPIC
UNAME_S := $(shell uname -s)

# Nome do output varia por SO
ifeq ($(OS),Windows_NT)
   SO_NAME = mandelbrot.dll
   SHARED_FLAG = -shared
else
   ifeq ($(UNAME_S),Darwin)
      SO_NAME = mandelbrot.dylib
      SHARED_FLAG = -shared
   else
      SO_NAME = mandelbrot.so
      SHARED_FLAG = -shared
   endif
endif

SRC_DIR = src

.PHONY: all run clean

all: $(SO_NAME)

$(SO_NAME): $(SRC_DIR)/mandelbrot.c $(SRC_DIR)/mandelbrot.h
	$(CC) $(CFLAGS) $(SHARED_FLAG) -o $@ $(SRC_DIR)/mandelbrot.c

run: all
	python3 $(SRC_DIR)/interface.py

clean:
	rm -f mandelbrot.so mandelbrot.dll mandelbrot.dylib
