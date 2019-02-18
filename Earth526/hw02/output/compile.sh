#!/bin/zsh
latexmk -pdf -pdflatex="xelatex -synctex=1 %S %O" -file-line-error -interaction=nonstopmode main.tex
