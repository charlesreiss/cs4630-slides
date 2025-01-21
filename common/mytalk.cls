\ProvidesClass{mytalk}[2018/09/08 version 0.03]
\NeedsTeXFormat{LaTeX2e}

\RequirePackage{silence}

\RequirePackage{xkeyval}

\RequirePackage{etoolbox}

\RequirePackage{pdfpages}

\RequirePackage{emoji}


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

\renewcommand<>{\sout}[1]{\alt#2{\beameroriginal{\sout}{#1}}{#1}}

\newfontfamily\sourcecodepro[
    UprightFont=*-Regular,
    ItalicFont=*-Italic,
    BoldFont=*-Semibold,
    BoldItalicFont=*-Semibold Italic]{Source Code Pro}

\newfontfamily\sourcecodeprolight[
    UprightFont=*-Regular,
    ItalicFont=*-Italic,
    BoldFont=*-Medium,
    BoldItalicFont=*-Medium Italic]{Source Code Pro}

\setmonofont[
    UprightFont=*-Regular,
    ItalicFont=*-Italic,
    BoldFont=*-Semibold,
    BoldItalicFont=*-Semibold Italic]{Source Code Pro}

%\ifluatex
%    \RequirePackage{luatexja}
%\else
%    \RequirePackage{xeCJK}
%\fi

% TIKZ
\usetikzlibrary{tikzmark}
\pgfdeclarelayer{bg}
\pgfdeclarelayer{fg}
\pgfsetlayers{bg,main,fg}


% HIGHLIGHT TOOLS
\newcounter{image}
\setcounter{image}{1}

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
    \setbeamerfont{alerted text}{shape=\ifmmode\relax\else\itshape\fi}%
    \setbeamercolor{alerted text}{fg=red!50!orange}%
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


\newcommand{\changelogmode}{
    \setbeamercolor{background canvas}{bg=blue!40!black,fg=blue!10!white}
    \setbeamercolor{normal text}{bg=blue!40!black,fg=blue!10!white}
    \setbeamercolor{itemize/enumerate body}{fg=white}
    \setbeamercolor{itemize/enumerate subbody}{fg=white}
    \setbeamercolor{titlelike}{bg=blue!40!black,fg=blue!10!white}
}

\makeatother

\iftoggle{heldback}{\newcommand<>{\maybeEmph}[1]{#1}}{\newcommand<>{\maybeEmph}[1]{\myemph#2{#1}}}

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

\endinput


