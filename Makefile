all:report.pdf
report.pdf:report.tex ref.bib
	pdflatex report.tex
	bibtex report.aux
	pdflatex report.tex
	pdflatex report.tex
.PHONY:clean
clean:
	rm -f *.aux *.log *.bbl *.blg *.fdb_latexmk *.fls *.out *.synctex.gz *.toc 