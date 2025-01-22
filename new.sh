#!/bin/bash
set -x
set -e
NAME=$1
mkdir $NAME
cat >$NAME/Makefile <<_END_
BASENAME=$NAME
LATEX=lualatex
include ../Makefile.inc
_END_

cat >$NAME/talk.tex <<'_END_'
\date{}
\title{}
\date{}
\begin{document}
\begin{frame}
    \titlepage
\end{frame}



\section{backup slides}
\begin{frame}{backup slides}
\end{frame}

\end{document}
_END_

cd $NAME && ln -s ../common/{mytalk.cls,talk-slides.tex,talk-slides-heldback.tex} .
