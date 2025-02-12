SLIDEDECKS = \
    logistics \
    intro \
    asm \
    x8664-encoding \
    exec-encoding \
    command-inj \
    virus \
    heur-detect \
    antianti \
    overflow \
    overflow-basic \
    overflow-smash \
    overflow-format \
    overflow-subterfuge \
    overflow-heap \
    uaf \
    mitigate \
    rop \
    static \
    taint \
    testing \
    bounds \
    betterpl \
    cfi \
    sandbox \
    symbolic \
    re-tools


all: $(patsubst %,_dist/%.pdf,$(SLIDEDECKS))

clean:
	rm -r _dist

_dist:
	mkdir _dist

_dist/%.pdf: % _dist .FORCE
	cd $< && make && cp talk-slides.pdf ../_dist/$<.pdf

.PHONY: all .FORCE
