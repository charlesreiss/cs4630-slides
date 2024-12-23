\ProvidesClass{mytalk}[2018/09/08 version 0.03]
\NeedsTeXFormat{LaTeX2e}

\RequirePackage{silence}

\RequirePackage{xkeyval}

\RequirePackage{etoolbox}

\newtoggle{heldback}
\togglefalse{heldback}

\newif\if@mytalkhandout\@mytalkhandoutfalse
\DeclareOptionX{handout}{%
    \@mytalkhandouttrue%
}
\DeclareOptionX{aspectratio}{%
    \PassOptionsToClass{aspectratio=#1}{beamer}%
}
\DeclareOptionX{showframe}{%
    \PassOptionsToClass{showframe}{geometry}%
}
\ProcessOptionsX\relax

\LoadClass[t,14pt,bookmarksdepth=5]{beamer}
\setcounter{tocdepth}{5}

\RequirePackage{fontspec}
\RequirePackage{tikz}
\RequirePackage{comment}
\RequirePackage{graphicx}
\RequirePackage{fancyvrb}
\RequirePackage{listings}
\RequirePackage{lmodern}
\RequirePackage[normalem]{ulem} % for sout
\RequirePackage[outputdir=latex.out]{minted}

\renewcommand<>{\sout}[1]{\alt#2{\beameroriginal{\sout}{#1}}{#1}}

\newfontfamily\sourcecodepro[
    UprightFont=*-Regular,
    ItalicFont=*-Regular It,
    BoldFont=*-Semibold,
    BoldItalicFont=*-Semibold It]{Source Code Pro}

\newfontfamily\sourcecodeprolight[
    UprightFont=*-Regular,
    ItalicFont=*-Regular It,
    BoldFont=*-Medium,
    BoldItalicFont=*-Medium It]{Source Code Pro}

\setmonofont[
    UprightFont=*-Regular,
    ItalicFont=*-RegularIt,
    BoldFont=*-Semibold,
    BoldItalicFont=*-Semibold It]{Source Code Pro}

\ifluatex
    \RequirePackage{luatexja}
\else
    \RequirePackage{xeCJK}
\fi

% TIKZ
\usetikzlibrary{tikzmark}
\pgfdeclarelayer{bg}
\pgfdeclarelayer{fg}
\pgfsetlayers{bg,main,fg}


% HIGHLIGHT TOOLS
\newcounter{image}
\setcounter{image}{1}

\newenvironment<>{btHighlight}[1][]
{\begin{onlyenv}#2\begingroup\tikzset{bt@Highlight@par/.style={#1}}\begin{lrbox}{\@tempboxa}}
{\end{lrbox}\bt@HL@box[bt@Highlight@par]{\@tempboxa}\endgroup\end{onlyenv}}

\newcommand<>\btHL[1][]{%
  \only#2{\begin{btHighlight}[#1]\bgroup\aftergroup\bt@HL@endenv}%
}
\def\bt@HL@endenv{%
  \end{btHighlight}%   
  \egroup %
}
\tikzset{
    btHLbox/.style={
        fill=red!30,outer sep=0pt,inner xsep=1pt, inner ysep=0pt, rounded corners=3pt
    },
}
\newcommand{\bt@HL@box}[2][]{%
  \tikz[#1]{%
    \pgfpathrectangle{\pgfpoint{1pt}{0pt}}{\pgfpoint{\wd #2}{\ht #2}}%
    \pgfusepath{use as bounding box}%
    \node[text width={},draw=none,anchor=base west, btHLbox, minimum height=\ht\strutbox+1pt,#1]{\raisebox{1pt}{\strut}\strut\usebox{#2}};
  }%
}

\tikzset{
    my callout/.style={draw,fill=blue!20!white,rectangle callout,callout absolute pointer=(pic cs:#1),below right=5pt of {pic cs:#1}},
    my callout2/.style={draw,fill=blue!20!white,rectangle callout,callout absolute pointer=(#1),below right=5pt of {#1}},
    ampersand replacement=\&,
    invisible/.style={opacity=0},
    visible on/.style={alt=#1{}{invisible}},
    alt/.code args={<#1>#2#3}{%
      \alt<#1>{\pgfkeysalso{#2}}{\pgfkeysalso{#3}} % \pgfkeysalso doesn't change the path
    },
    tight matrix node/.style={draw,rectangle,inner sep=1pt, outer sep=0pt,text width=1cm,minimum height=.4cm,anchor=center},
    tight matrix node noline/.style={rectangle,inner sep=1pt, outer sep=0pt,text width=1cm,minimum height=.4cm,anchor=center},
    tight matrix/.style={
        matrix of nodes,
        inner sep=1pt, outer sep=0pt,
        row sep=-\pgflinewidth,
        column sep=-\pgflinewidth,
        nodes={tight matrix node},
    },
    tight matrix no line/.style={
        matrix of nodes,
        inner sep=1pt, outer sep=0pt,
        row sep=-\pgflinewidth,
        column sep=-\pgflinewidth,
        nodes={tight matrix node noline},
    },
}

\makeatletter
\lst@CCPutMacro
    \lst@ProcessOther {"2A}{%
      \lst@ttfamily 
         {\raisebox{2pt}{*}}% used with ttfamily
         {\raisebox{2pt}{*}}}% used with other fonts
    \@empty\z@\@empty

\lstdefinelanguage
   [x8664gas]{Assembler}     % add a "x64" dialect of Assembler
   [x86masm]{Assembler} % based on the "x86masm" dialect
   % with these extra keywords:
   {morekeywords={CDQE,CQO,CMPSQ,CMPXCHG16B,JRCXZ,LODSQ,MOVSXD,%
                  POPFQ,PUSHFQ,SCASQ,STOSQ,IRETQ,RDTSCP,SWAPGS,.TEXT,.STRING,.ASCIZ,%
                  BEQ,LW,SW,LB,SB,ADDIU,J,BEQZ,BNEZ,BNE,%
                  MOVUPD,MULPD,MOVSD,MULSD,%
                  SHLADD,MOV,CMP.LT,TBIT.NZ,BR.RET.SPTK.MANY,%
                  ADDQ,POPQ,PUSHQ,RRMOVQ,MRMOVQ,RMMOVQ,IRMOVQ,%
                  <-,LL,SC,ADDI,ADDL,VMOVDQA,ADDQ,CMPL,JB,JBE,MOVL,CLTQ,
                  MOVW,PUSHW,MOV,ADD,SUB,INT,PUSH,MOV,ADD,REP,MOVSB,%
                  TESTQ,CMPQ,MOVL,MOVQ,ADDQ,JMPQ,XORQ,%
                  LEAQ,LEAL,LEA,RETQ,RET,POPL,POPW,PUSHL,PUSHW,%
                  LEAW,%
                  SUBQ,SYSCALL,.ASCII,CALLQ,MOVSLQ,JMP,ANDQ,SHRQ,MOVB,INCQ,TESTL,XORL,%
                  SHRL,LEAL,SARL,SUBL,IMULL,IMULQ,MOVDQU,PADDD,XORL,%
                  MOVZBL,MOVZB,SHRB,SRAL,SHRL,ANDL,%
                  CMOVNS,SRAL,SRAQ,MOVZBW,MOVZBQ,%
                  PADDW,PADDQ,MODUPS,MOVAPD,%
                  MOVL,RET,.GLOBL,%
                  },
    deletekeywords={eax,ebx,sp,si,cx,di,ds,cs,es,fs,dx,ax,bx,al,esi,ebp,ecx,rip,eip,edx,edi,rdi,esp},
    morecomment=[l]{\#},
    morecomment=[l]{\/\/},
    morecomment=[s]{/*}{*/},
    literate={<-}{$\leftarrow$}2{+}{$+$}1,
    sensitive=false,
    keepspaces=true} % et

\lstalias[]{myasm}[x8664gas]{Assembler}

\lstdefinelanguage{JavaScript}{
  keywords={typeof, new, true, false, catch, function, return, null, catch, switch, var, if, in, while, do, else, case, break},
  ndkeywords={class, export, boolean, throw, implements, import, this},
  sensitive=false,
  comment=[l]{//},
  morecomment=[s]{/*}{*/},
  morestring=[b]',
  morestring=[b]"
}

\errorcontextlines=3

\newcommand<>{\myemph}[1]{\alert#2{#1}}

\everymath{\displaystyle}

\newcommand{\mymainitemsep}{0.75em}
\patchcmd{\@listI}{\itemsep3\p@}{\itemsep\mymainitemsep}{}{}
\newcommand{\itemflush}{\vspace{-1em}\setlength{\itemindent}{0pt}\setlength{\leftmarginii}{1em}}

\usepackage{ifluatex}
\ifluatex
    \def\EmptyMapping{}
\else
    \def\EmptyMapping{\addfontfeatures{Mapping=}}
\fi

\newcommand{\keywordstyle}{\sourcecodeprolight\bfseries\color{blue!30!black}}
\newcommand{\stringstyle}{\color{blue!20!black}\ttfamily}

\lstset{
    language=C,
    basicstyle=\sourcecodepro\EmptyMapping,
    escapechar=`,
    keywordstyle=\keywordstyle\EmptyMapping,
    identifierstyle=\sourcecodepro\EmptyMapping,
    numberstyle=\small\color{black!70},
    commentstyle=\color{red!60!black}\ttfamily\itshape,
    stringstyle=\color{blue!20!black}\ttfamily,
    ndkeywordstyle=\bfseries\color{blue!30!black},
    upquote=true,
}



\lstdefinestyle{medium}{
    basicstyle=\sourcecodepro\EmptyMapping\fontsize{12}{13}\selectfont,
    keywordstyle=\sourcecodepro\EmptyMapping\fontsize{12}{13}\selectfont\keywordstyle,
}

\lstdefinestyle{small}{
    basicstyle=\sourcecodepro\EmptyMapping\small,
    keywordstyle=\sourcecodepro\EmptyMapping\small\keywordstyle,
}

\lstdefinestyle{smaller}{
    basicstyle=\sourcecodepro\EmptyMapping\fontsize{11}{12}\selectfont,
    keywordstyle=\sourcecodepro\EmptyMapping\fontsize{11}{12}\selectfont\keywordstyle,
}


\lstdefinestyle{script}{
    basicstyle=\sourcecodepro\EmptyMapping\scriptsize,
    keywordstyle=\sourcecodepro\EmptyMapping\scriptsize\bfseries,
}


\usetheme{boxes}
\usecolortheme{dolphin}
%\usefonttheme{structurebold}
\usefonttheme{professionalfonts}
\mode<presentation>%
{%
    %\setbeameroption{show notes on second screen=right}
    \setbeamercovered{invisible}%
    \setbeamerfont{frametitle}{size=\Large,series=\bfseries}%
    %\setbeamertemplate{frametitle}{\insertframetitle\vspace{.5cm}}%
    \setbeamertemplate{footline}{\color{black!70}\hfill\footnotesize\insertframenumber\hspace{.05cm}\vspace{.1cm}}%
    \setbeamertemplate{navigation symbols}{}%
    \setbeamertemplate{itemize items}{}% 
    \setbeamertemplate{enumerate subitem}{\alph{enumii}}%
    \setbeamertemplate{itemize subitem}{}% 
    \setbeamercolor*{item}{fg=black}%
    %\setbeamercolor*{frametitle}{fg=black}%
    %\setbeamercolor*{title}{fg=black}%
    \setbeamersize{text margin left=1em}%
    \setbeamerfont*{itemize/enumerate body}{size=\fontsize{15}{17}}%
    \setbeamerfont*{itemize/enumerate subbody}{size=\fontsize{13}{15}}%
    \setlength\leftmargini{0em}%
}
\tikzset{tikzmark prefix/.expand once=\thepage-\the\beamer@slideinframe-}
\mode<all>

\newcommand{\lmss}{\fontfamily{lmtt}\selectfont}
\renewcommand\textvisiblespace{{\lmss\char"2423}}

\DeclareGraphicsExtensions{.pdf,.png,.jpg}

\newcommand{\imagecredit}[1]{
    \begin{tikzpicture}[remember picture,overlay]
        \node (credit) [anchor=south east, align=left, font=\tiny,inner sep=0pt] at ($(current page.south east) + (-1cm,1mm)$) {#1};
    \end{tikzpicture}
}

\makeatother

\endinput
