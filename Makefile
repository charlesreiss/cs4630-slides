SLIDEDECKS = \
    logistics \
    intro \
    asm \
    x8664-encoding \
    exec-encoding \
    virus \
    heur-detect \
    antianti \
    overflow \
    mitigate \
    rop \
    static \
    taint \
    testing \
    bounds \
    betterpl \
    cfi \
    sandbox \
    symbolic


all: $(patsubst %,_dist/%.pdf,$(SLIDEDECKS))

clean:
	rm -r _dist

_dist:
	mkdir _dist

_dist/%.pdf: % _dist .FORCE
	cd $< && make && cp talk-slides.pdf ../_dist/$<.pdf

.PHONY: all .FORCE
