all: talk-slides.pdf

PUBLIC=../../website/slides/

%.pdf: %.tex .FORCE
	latexrun -W no-overfull --latex-cmd=$(LATEX) --latex-args=-shell-escape $<

copy: talk-slides.pdf
	cp talk-slides.pdf $(PUBLIC)/$(BASENAME)-slides.pdf
	chmod a+r $(PUBLIC)/$(BASENAME)-slides.pdf
	git add $(PUBLIC)/$(BASENAME)-slides.pdf

copy-heldback: talk-slides-heldback.pdf
	cp talk-slides-heldback.pdf $(PUBLIC)/$(BASENAME)-slides.pdf
	chmod a+r $(PUBLIC)/$(BASENAME)-slides.pdf
	git add $(PUBLIC)/$(BASENAME)-slides.pdf

clean:
	latexrun --clean-all

polls.csv: polls.yaml
	python3 ../make_poll.py polls.yaml polls.csv

.FORCE:

.PHONY: all clean .FORCE

# vim: ft=make
