filename = template

all: $(filename).tex
	mkdir tmp/ 
#	pdflatex --draftmode --output-directory=tmp $(filename).tex
#	bibtex tmp/$(filename)
#	pdflatex --draftmode --output-directory=tmp $(filename).tex
	pdflatex --output-directory=tmp $(filename).tex
	mv tmp/$(filename).pdf $(filename).pdf
	rm -r tmp/
