#!/bin/zsh

latexmk -pdf -pdflatex="lualatex -synctex=1 %S %O" -file-line-error -interaction=nons main.tex
