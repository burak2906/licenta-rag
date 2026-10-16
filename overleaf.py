\documentclass[12pt,a4paper]{report}

\usepackage[utf8]{inputenc} % pentru suport diacritice
% \usepackage[romanian]{babel} % setări pentru limba română
\renewcommand\familydefault{\sfdefault} % sans serif

\usepackage[utf8]{inputenc}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{ragged2e}
\usepackage{setspace}
\usepackage{float}
\usepackage{caption} 
\usepackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning}

\tikzstyle{startend} = [rectangle, rounded corners, minimum width=3.5cm, minimum height=1cm,text centered, draw=black, fill=white]
\tikzstyle{process} = [rectangle, minimum width=3.5cm, minimum height=1cm, text centered, draw=black, fill=white]
\tikzstyle{decision} = [diamond, aspect=2, text centered, draw=black, fill=white]
\tikzstyle{arrow} = [thick,->,>=stealth]

\usepackage[margin=2.54cm]{geometry} % dimensiuni pagină și margini
\usepackage{graphicx} % support the \includegraphics command and options

% formatting sections and subsections
\usepackage{textcase}
\usepackage[titletoc, title]{appendix}
\usepackage{titlesec}
\titleformat{\chapter}{\large\bfseries\MakeUppercase}{\thechapter}{2ex}{}[\vspace*{-1.5cm}]
\titleformat*{\section}{\large\bfseries}
\titleformat*{\subsection}{\large\bfseries}
\titleformat*{\subsubsection}{\large\bfseries}

\usepackage{chngcntr}
\counterwithout{figure}{chapter} % no chapter number in figure labels
\counterwithout{table}{chapter} % no chapter number in table labels
\counterwithout{equation}{chapter} % no chapter number in equation labels

\usepackage{booktabs} % for much better looking tables
\usepackage{url} % Useful for inserting web links nicely
\usepackage[bookmarks,unicode,hidelinks]{hyperref}

\usepackage{array} % for better arrays (eg matrices) in maths
\usepackage{paralist} % very flexible & customisable lists (eg. enumerate/itemize, etc.)
\usepackage{verbatim} % adds environment for commenting out blocks of text & for better verbatim
\usepackage{subfig} % make it possible to include more than one captioned figure/table in a single float
\usepackage{enumitem}
\setlist{noitemsep}

% packages used for citations
\usepackage{apacite}
\usepackage{natbib}

\usepackage{xcolor}
\usepackage{listings}
\lstset{language=Python,basicstyle={\bfseries \color{black}},keywordstyle={\bfseries \color{blue}}}

%%% HEADERS & FOOTERS
\usepackage{fancyhdr}
\pagestyle{empty}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\lhead{}\chead{}\rhead{}
\lfoot{}\cfoot{\thepage}\rfoot{}

\newcommand{\HeaderLineSpace}{-0.25cm}

\newcommand{\UniTextEN}{National University of Science and Technology\\ POLITEHNICA Bucharest\\
Faculty of Automatic Control and Computers\\
Computer Science and Engineering Department\\}
\newcommand{\DiplomaEN}{DIPLOMA PROJECT}
\newcommand{\AdvisorEN}{Thesis advisors:}
\newcommand{\BucEN}{BUCHAREST}

\newcommand{\frontPage}[6]{
\begin{titlepage}
\begin{center}
{\Large #1}  % header (university, faculty, department)
\vspace{50pt}
\begin{tabular}{ccc}
\includegraphics[height=3cm]{pics/UNST Poli.png} & 
\includegraphics[height=3cm]{pics/A&C.png} & 
\includegraphics[height=3cm]{pics/UPB NLP.png}
\end{tabular}

\vspace{105pt}
{\Huge #2}\\                             % diploma project text
\vspace{40pt}
{\Large #3}\\ \vspace{0pt}               % project title
\vspace{40pt}
{\LARGE \Name}\\                         % student name
\end{center}
\vspace{60pt}
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}p{6cm}r}
&{\large\textbf{#5}}\vspace{10pt}\\      % scientific advisor
&{\large \AdvisorA}\\                    % advisor name A
\end{tabular*}
\vspace{20pt}
\begin{center}
{\large\textbf{#6}}\\
\vspace{0pt}
{\normalsize \Year}
\end{center}
\end{titlepage}
}

\newcommand{\frontPageEN}{\frontPage{\UniTextEN}{\DiplomaEN}{\ProjectTitleEN}{\ProjectSubtitleEN}{\AdvisorEN}{\BucEN}}

\linespread{1.15}
\setlength\parindent{0pt}
\setlength\parskip{.28cm}

%% Abstract macro
\newcommand{\AbstractPage}{
\begin{titlepage}

\thispagestyle{fancy}\setcounter{page}{5}
\clearpage\phantomsection\addcontentsline{toc}{chapter}{Abstract}

\textbf{\large ABSTRACT}\par
\AbstractEN \vfill
\textbf{\large REZUMAT}\par
\AbstractRO\par\vfill
\end{titlepage}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%%          End of template definitions
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\ProjectTitleEN}{A Multi-Modal Framework for Solving Car Driving Exam Questions: Integrating Text, Image, and Contextual Analysis}
\newcommand{\Name}{Buracu Stefan-Paul}
\newcommand{\AdvisorA}{S.l. dr. ing. Laurențiu-Marian Neagu}
\newcommand{\Year}{2025}

% Setări document
\title{Proiect de diplomă}
\author{\Name}
\date{\Year}

%%
%%   Câmpurile aferente rezumatului
%%
\newcommand{\AbstractEN}{
Large Language Models (LLMs) are increasingly used in educational domains due to the fast evolution of artificial intelligence. These models are commonly utilized by students to prepare for exams and obtain answers to questions specific to a given subject. In Romania, the theoretical part of the driving license exam consists of Multiple-Choice Questions (MCQ) selected from a predefined set. The objective is building a multi-modal framework for solving car driving  questions. To study the knowledge of LLMs in this area, two models, Gemma3-27B and LLaVA:34B, are analyzed under three scenarios. The scenarios are: a simple version where the model receives only the question and the answer options, a version in which each question is accompanied by relevant legal context retrieved from the Road Safety Legislation through semantic search (using ChromaDB and MiniLM embeddings), and a version where the textual context from the previous point is also accompanied by official definitions extracted by automatic detection of traffic signs from images with YOLOv8. The conclusion is a comparison of the accuracy of the responses in the described conditions and an analysis of whether the context added through a Retrieval-Augmented Generation (RAG) system can improve the results. 

}


\newcommand{\AbstractRO}{
Modele lingvistice de mari dimensiuni (LLMs) sunt din ce în ce mai folosite in domenii educaționale din cauza evoluției inteligenței artificiale. Acestea sunt des utilizate de studenți pentru a se pregati pentru un examen și a obține răspunsuri la întrebari specifice domeniului dorit. In Romania, partea teoretică a examenului pentru permisul de conducere este formata din întrebări grila dintr-un set de întrebări prestabilit. Obiectivul este dezvoltarea unui framework multimodal pentru rezolvarea întrebărilor auto. Pentru a studia cunoștințele LLM-urilor in aceasta arie și pentru a stabili care este mai potrivit framework-ului, am analizat doua modele, Gemma3:27B si LLaVA:34B, in 3 scenarii diferite. Scenariile sunt: o variantă simplă în care modelul primește doar întrebarea și opțiunile de răspuns, o variantă în care fiecare întrebare este însoțită de un context legal relevant extras din Codul Rutier prin căutare semantică (folosind ChromaDB și embedding-uri MiniLM), și o variantă în care contextul textual de la punctul anterior este însoțit și de definiții oficiale extrase prin dectectie automata a semnelor rutiere din imagini prin YOLOv8. Concluzia este o comparare a acurateții răspunsurilor in condițiile descrise și o anliza dacă adăugarea contextului printr-un sistem de tip Retrieval-Augmented Generation (RAG) poate îmbunătăți rezultatele. 
 
\vspace{3\baselineskip}
}


\begin{document}
\pagenumbering{roman}
\frontPageEN
\begingroup
\linespread{1}
\tableofcontents
\endgroup

% Keep the list of figures and the list of tables on the same page.
\pagestyle{fancy}
\listoffigures\addcontentsline{toc}{chapter}{List of figures}
\begingroup
\let\clearpage\relax
\listoftables\addcontentsline{toc}{chapter}{List of tables}
\endgroup

% Include the abstract page. See this definition if page numbers are wrong.
\AbstractPage

% poate fi comentata sau stearsa
% \ThanksPage

% Start the normal page numbering.
\pagenumbering{arabic}

% Textul licentei incepe de aici
\chapter{Introduction}\pagestyle{fancy}

\section{Context}
In recent years, Artificial Intelligence (AI) has become increasingly present in the field of education, offering new ways to personalize learning, automate assessments, and extend access to knowledge. As a result, AI is now used in almost any context in which people want to get a better grasp on a subject that brings difficulties, or to find answers to questions that are causing trouble and uncertainty. Large Language Models (LLMs), such as ChatGPT, Gemma or DeepSeek, revolutionized human-computer interaction in natural language processing (NLP) tasks through their capability to understand and interpret human language. 

 

In Romania, the process of obtaining a driving license includes a mandatory theoretical phase, that is based on standardized multiple-choice questions provided by G.D.D.L.R. (General Directorate for Driving Licenses and Registrations; Romanian: Direcția Generală pentru Permise de Conducere și Înmatriculări) \citep{dlexam} . In this part of the exam, the examinee must answer 26 Multiple-Choice Questions (MCQ) questions. To pass it, 22 correct answers are required. These questions cover legal aspects of the Road Safety Legislation, traffic signals, car mechanics, and some are accompanied by images that include road signs or traffic scenarios. 

 

To prepare for this exam, candidates study from approved online courses, which cover traffic laws, car mechanics, first aid, eco-driving, and preventive behavior \citep{scoalarutiera}, or by reading books in accordance with Road Safety Legislation. Last updated on 05.02.2025, the legislation includes 137 articles from the Rode Traffic Code \citep{drpciv_cod} and 224 articles from the Driving Regulation \citep{drpciv_regulament}. One strategy to pass this test includes iterating the questions multiple times to understand the concepts, because the Road Safety Legislation is full of juridical terms that are hard to understand at first encounter for someone unfamiliar with this field. These learning strategies can lead to demotivation or inefficiency for some people considering the workload. 

 

An easier and more modern assisted method that can contribute significantly to the future drivers’ education would be utilizing an automated system based on LLMs, capable of understanding the questions in order to answer them and give the reasoning behind the answer. 

 

 
 
\section{Problem Statement}
Even though the learning methods for the driving license exam are becoming more and more diverse, most of the candidates rely on memorizing the answers to the G.D.D.L.R. questions by going through them multiple times. There is no correlation in this process with the theory that can be studied. Since all the questions that are eligible to be in the exam can be found online, learners are prompted toward using this method, even though in most cases people fail to understand the logic behind the questions. The complexity of the Road Safety Legislation is again another problem, if it's not followed by any adaptive feedback that can help the reader. 

 

The best alternative that exists to this is going through the questions on a website that has an online simulation of the exam, where the user receives explanations for the last answered question even if it was correct or incorrect \citep{chestionareaz}. In this way, there is an association between the questions and the stated logic behind the correct answer that can help through the learning process. The problem occurring in these scenarios is the additional search for supplementary information if the standard explanation is not enough. 

 

Furthermore, the recent progress regarding conversational Artificial Intelligence is extending the possibilities for using virtual agents capable of answering users’ questions in real time, offering indications or clarifications. Theoretically, a system like this could be integrated into a dedicated platform that would enhance the learning process for future drivers by fostering an in-depth understanding of the information. 

 

With all of this considered, there is no solution that integrates this sort of AI agent in an official and tested way. There are some LLMs that are free to access online and can answer the G.D.D.L.R. questions, but there is not a single clear evaluation study that can confirm the given answers are in fact correct and are supported by real and relevant justification. More than this, the limitations of these LLMs are yet to be studied when it comes to their capabilities to acquire context for the questions and images that come with them. So here comes the main question of this research: can these LLMs answer correctly the G.D.D.L.R. questions? If not, how can their performance be optimized? 

 
\section{Objectives}
 
The main purpose of this paper is the performance evaluation of a multimodal framework based on LLMs, capable of answering the G.D.D.L.R. multiple-choice questions, with or without an additional context. The study aims to determine how LLMs can be used in order to correctly answer questions repeatedly with given context from the Road Safety Legislation and visual interpretation of the traffic signs from two auxiliary sources. 

An analysis of the LLMs’ capacities to answer correctly to the questions in the zero-shot scenario will be made and studied by finding the most relevant context for the questions’ answers, so a conclusion can be drawn in this field. 

 

Going further, another objective consists of a Retrieval Augmented Generation component that can extract the information that will be sent as context for the prompt, so the models will obtain better results. For this purpose, a semantic search and a vectorial database will be used to prove the relevance of context-driven generation as a means of increasing the accuracy of responses. 

 

As a good number of questions have an image linked with them, this should be treated with visual recognition. As traffic signs come up in the majority of visual questions, the study wants to detect them in the most efficient way. 

 

The final and most important objective represents the comparison between the two models Gemma3:27B \citep{gemma} and LLaVA:34B \citep{llava}, used for this study in all 3 scenarios: without context, with textual context, and with both textual and visual context. This comparison will determine the better model for the QA task. 

\section{Thesis Structure}
This paper is structured into six chapters, followed by references. Every chapter has its contribution to the proposed research understanding. 

 

The first chapter has the role of introducing the reader to the context of the paper, justifying the importance of the subject, pointing out the problems that the research brings, and establishing the objectives. 

 

The second chapter offers an overview of other studies concluded beforehand that include utilization of LLMs in educational or juridical contexts and RAG techniques implementations for optimal information selection from external sources. In this chapter, multimodal approaches are presented in QA tasks and other similar applications with visual recognition implemented in the automotive field. 

 

The third chapter describes the proposed methodology, the architectural structure of the framework, implemented software components, the structure of the dataset, and how the textual and visual context are combined in the LLM prompting. 

 

The fourth chapter presents experiments and results. The three scenarios of the testing are treated (without context, with textual context, and textual and visual context combined), and the evaluation metrics are interpreted (precision, recall, F1-score). 

 

The fifth chapter is about the discussion between the two models, and a critical analysis of the experimental results is shown, explaining the impact in each type of context situation. The framework’s limitations are also detailed here. 

 

The sixth and final chapter ends with the conclusions of the research and future directions that are possible for extending the studies.  

 

%---------------------------
\chapter{State of the art}
This chapter presents existing similar implementations regarding the subject discussed. Artificial Intelligence has helped develop many NLP applications for extracting crucial information from different sources and for visual processing. These two algorithms are seen together often in scientific, educational, or juridical areas, using RAG (Retrieval-Augmented Generation) for multimodal language and object detection. Our proposed framework mixes text and image processing in order to answer automatically the driving license exam questions, using extracted context from the Road Safety Legislation and also traffic signs interpretation. For this to be solved, relevant research and comparison will be presented from different studies that include RAG, LLMs and their reasoning abilities, and modern methods for detecting visual objects.



\section{Retrieval-Augmented Generation (RAG)}
 

Retrieval-Augmented Generation or RAG is a hybrid technique that came to developers’ attention first in the area of Artificial Intelligence in 2020 \citep{lewis2020retrieval}. As the name implies, it has two components: a retriever that extracts relevant documents from a database and a generator, more precisely a LLM (in this study Gemma3:27B and LLaVA:34B), that generates answers based on a question and given context. The main objective is improving the performance of Large Language Models in order for them to precisely answer a question without having to know all parameters of knowledge, and only the most important ones, reducing unnecessary calculations. This kind of approach is mostly used in domains that require exact information for finding a precise answer due to the amount of similar data, such as law, medicine or, like in this case, traffic education. For example, in the study by \citet{louis2024interpretable}, RAG is applied in the juridic area for solving difficult questions, giving more than just an answer, but also an explanation from extracted sources from the legal corpus. This shows how capable RAG is in fields like the study presents. 

 

In this study, the Retrieval-Augmented Generation is used in the implementation of context-gaining processes based on the Road Safety Legislation, as well as the visual part, selecting indications for traffic signs that are identified in the G.D.D.L.R. Multiple-Choice Questions with an image. With semantic search using ChromaDB \citep{chroma} and SentenceTransformers (MiniLM) \citep{minilm} with CrossEncoder \citep{crossencoder} reranking, the best context will be retrieved to complete the question for a better understanding and for receiving a correct response from the LLM. A similar approach is described by \citet{masuda2011semantic}. The article proposes an architecture for semantic search based on Natural Language Processing, such as lemmatization, entity identification, and syntactic analysis. Even though the implemented system presented in this thesis is using dense embeddings for vectorization and semantic similarity, the idea remains the same, namely the importance of obtaining a relevant and precise context from a corpus of knowledge by understanding its content, not by exact comparison. 

 

MiniLM is used with a CrossEncoder for a better selection of the relevant context, the reason behind this being that the questions and the articles that will be chosen with RAG and written in Romanian, a difficult language for automatic processing, as \citet{pais2021depth} presents. The Romanian language brings significant challenges in NLP, like morphological ambiguity and lack of standardized resources. All this being considered, a multilingual solution is necessary. 

 

In addition, for questions containing an image, visual detection with YOLOv8 is integrated, along with indexing made in ChromaDB for finding the official definitions of each traffic sign associated with the images in order to improve the context. The retrieved definitions are also added to the context in the final prompt that is given to the LLM. All this combined makes a multimodal RAG architecture. \citet{zhang2023multimodal} are also highlighting in their study that integration of multimodal retrieval is considerately increasing the results in general tasks. 

 

Amongst RAG strategies used in Large Language Models there are: classic RAG, incremental RAG (iRAG), and adaptive RAG. The study conducted by \citet{gao2023retrieval} showcases the differences between these models by analyzing their performances and resource consumption for each method. The classic one relies on a fixed number of documents based on the similarities with the questions, concatenated in the same prompt. This variant can produce informational noise because the chances of extracting articles that are not connected in relevance to the questions’ meaning are high. The incremental approach gives a score of relevance (with semantic similarity or reranking), that makes an article eligible for selection if it is identified with a score that exceeds a predefined threshold. This is seen as an extra verification filter for the most relevant context. The adaptive method extends this idea by using iterative feedback from the LLM to strengthen the context with successive steps based on the generated response. Even though the last option seems the most effective, it is also the most resource intensive. The method used in this project is based on the incremental RAG, because it selects articles based on their similarity score, refined through reranking, so the context bypassing the relevance threshold is included. In a different approach than the classic RAG, the threshold and the maximum number of selected articles after the descending sorting based on the similarities scores are selected with experiments. This solution is inspired by a lecture about iRAG which proposes a progressive selection to obtain better accuracy and scalability \citep{adnan2024irag}.
\section{Multimodal questions}
 

Another extension from the RAG as an alternative architecture is represented in a study made by \citet{chenmultimodal}, which presents a system that retrieves important images for a more compound context for the questions and adds them to the textual part of the prompting in a multimodal QA model. This architecture shows the importance of correct imagistic understanding in the process of receiving a correct answer from the LLM, this thinking method is used partially in the study of G.D.D.L.R. multiple-choice questions in regard to interpreting the visual part of the question. 

 

Even more in this field of studies, \citet{suri2024visdom} is proposing a QA complex system on documents with a large number of visual components, that run in parallel on two RAG flows, a visual one and a textual one. This architecture introduces a fusion between the answers retrieved from each type of content, also imposing consistency constraints between them. Compared to methods such as Long Context or standard RAG, VisDoMRAG offers better performances by between 2.1\% and 52\% on all benchmarks tested, depending on the size of the model used and the complexity of the task, as seen below in Figure~\ref{fig:visdomrag}.

\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{pics/visdomrag.png}
\caption{\textit{Comparison between Long Context and VisDoMRAG on multiple QA benchmarks. Figure adapted from \citet{suri2024visdom}}}
\label{fig:visdomrag}
\end{figure}

Although there are impressive improvements in this practice compared to unimodal systems, the structure is of increased complexity, and the implementation through multiple steps makes it not the ideal choice in all cases. 

 
A more general framework for applying multimodal models in driving tasks is presented by \citet{gao2024survey}. Authors present a complete synthesis of how fundamental models, such as LLMs, VFMs, and multimodal architectures, are used in the context of autonomous driving. Among the applications highlighted are visual scene understanding, object segmentation, traffic sign detection, behavioral prediction and even textual explanation generation. This approach supports the direction of this study to deal with the textual context among the visual ones, pointing out the attention on the limitations of these methods in real scenarios, observed in the tests performed later. A representation of the presented pipeline for a LLM in decision making system belonging to the authors of the study is included below in Figure~\ref{fig:llm-decision-pipeline}.

\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{pics/schemaframeworkmultimodal.png}
\caption{\textit{Example of a multimodal decision-making pipeline involving an LLM, adapted from \citet{gao2024survey}.}}
\label{fig:llm-decision-pipeline}
\end{figure}

\citet{zhang2023multimodal} propose an architecture called Multimodal Chain-of-Thoughts. This approach consists in two steps: first the model generates intermediate reasoning based on the question and the image attached, and then, using the reasoning, it produces a final answer. The method achieved remarkable performances, surpassing even GPT-3.5 and the average human score, with a model with under 1 billion parameters. The relevance of this article consists in the fact that it strengthens the idea that integrating visual information into step-by-step reasoning significantly increases accuracy in educational tasks. A plot showcasing the accuracy comparison can be seen in Figure~\ref{fig:vision-modality-comparison}.

\begin{figure}[H]
\centering
\includegraphics[width=0.6\textwidth]{pics/acurateti.png}
\caption{\textit{Answer accuracy with and without vision modality across different LLM sizes, adapted from \citet{zhang2023multimodal}.}}
\label{fig:vision-modality-comparison}
\end{figure}
As a relevant study regarding the visual part of information, the thesis made by \citet{zheng2025retrieval}, presents in detail how a RAG system can be extended to support understanding and generating content in visual format, not just textual. This paper comes up with a proposal for a multimodal architecture for visual context integration in the RAG strategy, in the field of computer vision. This article played a major role in the decision-making process for the integration of the visual elements in the proposed model, using one of the two methods: CLIP \citep{clip} and YOLOv8 \citep{yolov8}. 

 

In the official questionnaires, the MCQs (Multiple Choice Questions) might include images depicting certain symbols (e.g., circulation signs) and certain real-world corner-case situations (i.e., top-view images of roads and intersections, or first-person view). These images are meant to test the diver's decision-making abilities, and their advanced understanding is crucial for the development of driving skills. CLIP can help extract image embeddings and search in a visual similarity collection of signs indexed in ChromaDB. YOLOv8, on the other hand, is used for the visual recognition of multiple road signs in one image, pretrained with pictures with the signs in diverse positions. Testing the accuracy with each method, YOLOv8 had better results than CLIP. This is due to the nature of the images used in the G.D.D.L.R. questions. For the CLIP model, the presence of several traffic signs or distorted, scaled-down images of the signs created confusion in the model’s output. With all this considered, YOLOv8 has been chosen for the best visual detection in this study case. 

 

 

CLIP (Contrastive Language-Image Pre-training) is a multimodal model that learns simultaneously from images and the text associated with them, having the objective of achieving a minimum cosine distance between the embedding of an image and the corresponding text and a maximum one against the unrepresentative ones \citep{radford2021learning}. CLIP does not require additional data training, since the model is pre-trained on over 400 million pairs (image, text) extracted from the internet, which allows it to generalize on a wide range of visual tasks. Its zero-shot classification capacity makes the model applicable without fine-tuning, proving to be competitive, or even superior in 16 of the 27 benchmarks tested by the authors, the scores obtained in the study discussed are shown in Figure~\ref{fig:clip-benchmark}. Positive values indicate benchmarks where CLIP outperforms the baseline.


\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{pics/cliprezultate.png}
\caption{\textit{Zero-shot CLIP performance compared to linear probe on ResNet50 across 27 benchmarks, adapted from \citet{radford2021learning}.}}
\label{fig:clip-benchmark}
\end{figure}



These results were obtained in comparison with a supervised logistic classifier trained on features extracted from the ResNet-50 model \citep{resnet50hf}, a standard in computer vision. In cases where visual differences are subtle and not easily deduced from the text, CLIP can get tangled in texts, which is why it didn’t end up in the final version. 

 

Other than the CPIL solution, other studies proposed different ways for visual context integration in RAG systems. The thesis written by \citet{zhang2025fine} introduced a fine-grained RAG used with visual content assisted questions, where knowledge units associate images with a text description. In this way the relevant information is subtracted easier, making the procedure better in efficiency when it comes to more complex visual elements, such as symbols, graphics, or diagrams. 

 

In the next part, there will be studies related to the method chosen for the visual context, namely YOLOv8. 



\section{Visual recognition with YOLOv8}
Continuing the topic discussed, in the context of this thesis, each question containing images has been contextualized with automatic road sign detection with the afferent definition from the ChromaDB collection used. For this, the YOLOv8 model (You Only Look Once version 8), a one-step object detection model, which offers precise predictions in real time, was used. 

 

YOLOv8 allows more objects to be identified from a single image, returning the class and coordinates for each object found. Considering this, it was the perfect fit for this study because as we said prior, the G.D.D.L.R. questions can have more than one road sign in a single picture, and all of them represent crucial information that the LLM needs to know to maximize a correct response. 

 

A paper that perfectly illustrates this choice is the one by \citet{ibrahim2025enhancing}, which is precisely focused on the recognition of road signs and makes a detailed analysis on the performance of YOLOv8 model compared to other known models, such as YOLOv5, SSD and Faster R-CNN. Authors managed to demonstrate with experiments that YOLOv8 has a superior accuracy in road signs detection, especially in difficult scenarios where the sign is not clear, or is hard to observe, or even where the pictures are from strange angles or are lacking brightness. The YOLOv8 model in the improved version has obtained the best results in all tested metrics: 93\% precision, 90\% recall, a 45FPS detection rate and a mAP score (mean Average Precision) of 91.5\%, significantly better than the others. This information can be found in Table~\ref{tab:compare_matrics}. 

\begin{table}[H]
\centering
\caption{\textit{Comparative Performance Metrics \citep{ibrahim2025enhancing}}}
\label{tab:compare_matrics}
\vspace{2mm}
\begin{tabular}{l c c c c}
\hline
\textbf{Model} & \textbf{mAP (\%)} & \textbf{Precision (\%)} & \textbf{Recall (\%)} & \textbf{FPS} \\
\hline
Faster R-CNN     & 88.0 & 90 & 87 & 20 \\
SSD              & 86.5 & 88 & 84 & 35 \\
YOLOv5           & 87.3 & 89 & 85 & 42 \\
Enhanced YOLOv8  & 91.5 & 93 & 90 & 45 \\
\hline
\end{tabular}
\end{table}


This model is remarkable for its versatility in its generalization on diverse datasets, which recommends it in practical applications, like this research. 

 

Another recent study that encourages this visual architectural choice, YOLOv8, is the one by \citet{sah2025advancing}, which proposes an advanced multimodal framework for autonomous vehicles, integrating road sign and lane detection with an LLM model for contextual understanding. Authors used YOLOv8 for accurate detection of road signs in real images, in adverse weather conditions, traffic or barely visible signs. The presented pipeline takes the visual information extracted by YOLOv8 and is transforming it into textual information, later processed by a LLM for a full understanding of the whole scene in order to decide the behavior of the vehicle. For a better understanding, a representation of results from this model can be seen in the next Figure~\ref{fig:yolov8-llm-results}.
\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{pics/exemplerecunoasteresemne.png}
\caption{\textit{Visual detection and scene understanding using YOLOv8 integrated with an LLM for autonomous driving decisions. Image adapted from \citet{sah2025advancing}.}}
\label{fig:yolov8-llm-results}
\end{figure}


This presented approach strengthens the efficiency of the YOLOv8 architecture in significant visual signal extraction and shows its compatibility with LLMs, even in complex scenarios for applications. This system is in analogy with the research on the G.D.D.L.R. questions, having a similar strategy that was part of the decision to associate a textual definition context to the road signs detected with YOLOv8. Now the model can answer not only using Road Safety Legislation as information, but also accessible information adapted from visual information. 

 

More than all, the study by \citet{gao2024survey} offers a broad perspective about how relevant visual detection and its integration in the general reasoning are, in how foundation models are applied in autonomous driving. This study presents the advantages of all hybrid architectures that mix convolutional networks, such as YOLOv8, for visual perception, with LLMs capable of giving explanations and reasoning based on extracted information. YOLOv8 is presented as being ideal for road signs, obstacles and other traffic components detection in real time, because of its optimization in low latency and easy integration into embedded systems. Even more, this thesis highlights the important role of visual detection as a part of a multimodal pipeline, in which the results are supposed to be transformed into textual elements in order to be processed by a LLM. Exactly the same approach of combining the visual perception and the reasoning into a text form is presented into this paper, where YOLOv8 detects traffic signs and their definition is transmitted in a textual form to a LLM in order to receive better results to G.D.D.L.R. questions.  

 

Therefore, even though different multimodal solutions have been analyzed, in order to solve the problem regarding G.D.D.L.R. questions, as presented in the beginning, the most efficient approach is by using a trained YOLOv8 model for road signs recognition. For the type of pictures that are included in the driving exam questions, YOLOv8 has a higher performance than CLIP. 






%---------------------------
\chapter{Method}
This chapter describes the complete architecture of the automatic evaluation framework for Romanian driving exam questions. The analysis goes in-depth into the components and used technologies, along with the motivation for each choice. The proposed system is multimodal, combining natural language processing with visual recognition, contextual augmentation, and automatic evaluation of the LLMs used. 
\section{Dataset}
 

In this project, the dataset used for training, testing, and validating the solution were automatically scraped from the platform of the Directorate of Driving License and Vehicle Registration (Romanian: Directia Regim Permise de Conducere si Inmatriculare a Vehiculelor – D.R.P.C.I.V.) school, from the category B, questions used in the real theoretical exam for obtaining a driving license \citep{scoaladrpciv}. 

 
\subsection{G.D.D.L.R. questions}

All questions are saved in a MongoDB \citep{mongodb} collection imported locally in a standardized JSON format for an easier look at the experiment. Each question has the following fields: the question text, three answer options (A, B, C), the correct answer(s), a unique identifier provided by MongoDB, and the path to an associated image if it exists. 

 

A total of 1212 unique questions were collected, out of which 385 include an image, and the rest of 827 are only based on the text part. This dataset is saved in a MongoDB collection for a full overview of all questions explored in the project. 

 

The motivation behind this dataset is the fact that it includes all possible questions that can be seen in the official driving license exam, making this a reliable benchmark for evaluation. It captures the capabilities of a LLM in a real-world educational domain that includes both textual and visual components. Some sample questions can be seen in Table~\ref{tab:samplequestions}.

\begin{table}[H]
\centering
\caption{\textit{Sample Questions from G.D.D.L.R. Dataset}}
\label{tab:samplequestions}
\begin{tabularx}{\textwidth}{@{} l X X c c @{}}
\toprule
\textbf{ID} & \textbf{Question Text} & \textbf{Options} & \textbf{Answer} & \textbf{Image} \\
\midrule
Q1 & Când ninge abundent veți folosi: 
   & A. luminile de poziție \newline B. claxonul \newline C. luminile de întâlnire ale farurilor
   & C & Yes \\
   
Q2 & Cum trebuie să procedeze conducătorul de vehicul atunci când circulă pe un drum cu trei sau mai multe benzi pe sens?
   & A. să circule pe banda situată lângă acostament \newline B. să nu circule pe liniile de tramvai \newline C. să circule pe banda a doua, respectiv a treia, cu o viteză mai mică de 100 km/h
   & A & No \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{Auxiliary Corpus for ChromaDB}

In order to provide legal context for LLMs to answer questions using the retrieval-augmented generation method, there were also added two auxiliary corpora. The first one includes 671 articles from the Romanian Road Safety Legislation (Romanian: Codul Rutier) \citep{drpciv_cod} and online courses explanations \citep{scoalarutiera}, that were extracted, parsed into individual paragraphs, so that each has an own individual meaning. The second one stores 257 official definitions for all existing traffic signs \citep{semne_rutiere}. The corpus made up of law regulations is used for the textual RAG context, and the definitions are added in the context when YOLOv8 detects the corresponding sign. 

 

Both corpora are indexed in ChromaDB, a vector database optimized for semantic search, and saved locally in JSON objects for better visualization. To index the database, the all-MiniLM-L6-v2 embeddings from SentenceTransformers were utilized, due to their extensive and efficient semantic similarity search between questions and the most useful legal context from an article. Some example articles are shown in Table~\ref{tab:samplearticles}, and some road sign definitions in Table~\ref{tab:samplesigns}.

\begin{table}[H]
\centering
\caption{\textit{Sample Articles from Romanian Road Safety Legislation}}
\label{tab:samplearticles}
\begin{tabularx}{\textwidth}{@{}l X@{}}
\toprule
\textbf{Article} & \textbf{Content} \\
\midrule
OUG - Articolul 63, alin.(4) & Se consideră parcare staționarea vehiculelor în spații special amenajate sau stabilite și semnalizate corespunzător. \\

Regulament - Articolul 51, alin.(1) & Semnalul de culoare verde permite trecerea. \\

Regulament - Articolul 52, alin.(1) & Semnalul de culoare roșie interzice trecerea. \\
\bottomrule
\end{tabularx}
\end{table}


\begin{table}[H]
\centering
\caption{\textit{Sample Traffic Sign Definitions}}
\label{tab:samplesigns}
\begin{tabularx}{\textwidth}{@{}l X@{}}
\toprule
\textbf{Traffic Sign} & \textbf{Definition} \\
\midrule
Indicator Port & Indicator Port: Se amplasează în apropierea unui port. \\
Indicator Gară & Indicator Gară: Se amplasează în apropierea unei gări. \\
\bottomrule
\end{tabularx}
\end{table}


\subsection{Data preprocessing}
Before using the data in the multi-modal pipeline, the questions are going through two preprocessing operations to ensure consistency and compatibility with the overall framework in the later automated testing. 

 

The first operation is text normalization and diacritic removal, applied to prevent errors of misinterpretation in the semantic embeddings. The text is converted to a unified form using Unicode NFD \citep{unicodedata} and special characters elimination. The second verification is only for the questions containing the \texttt{image\_local\_path} field and is validating the image is in fact existing physically in the local directory to prevent errors. 

 

In addition, the system provides an extension of the MongoDB question documents, created automatically after receiving the LLM’s responses. This supplementary field, a structured JSON node, is used to store the responses generated by LLMs for an easier evaluation from each model (LLaVA:34B, Gemma3:27B). For each LLM as an entry we have fields that include: the LLM answer without a context, the LLM answer with the selected context (textual and/or/without visual), the source of the context (crossencode, yolo, fallback), and the context used in the prompt. 

 

Using these fields, we have all we need for an automated evaluation workflow with MongoDB as the storage system. 
\section{Architecture}
The proposed framework is comprised of multiple independent modules that cooperate in a pipeline with the objective to automatically answer to the Romanian driving license exam questions, using both visual and textual information. Architecturally speaking, this is a multi-modal framework that uses natural language processing techniques (NLP), computer vision (CV), contextual search (RAG), and answer generation with LLMs. 

 

Table~\ref{tab:components} provides an overview of the main components of the framework’s architecture. Each row specifies the responsibilities of a given module. 


\begin{table}[H]
\centering
\caption{\textit{Descriptions of Each System Component}}
\label{tab:components}
\begin{tabularx}{\textwidth}{@{} >{\RaggedRight\arraybackslash}p{4cm} >{\RaggedRight\arraybackslash}X @{}}
\toprule
\textbf{Component} & \textbf{Description} \\
\midrule
MongoDB & Stores all questions in JSON format, including text, options, and images. \\

Preprocessing & Normalizes input text and verifies the presence and validity of any attached image. \\

Textual context retrieval & Retrieves relevant context using semantic search over documents indexed in ChromaDB. \\

Reranking with CrossEncoder & Scores and ranks retrieved documents based on semantic relevance to refine context selection. \\

Visual detection with YOLOv8 & Detects and identifies traffic signs in input images to retrieve their definitions. \\

Prompt generation & Builds a structured prompt by combining the question, answer choices, and retrieved context. \\

LLM inference & Generates an answer using the selected large language model (e.g., LLaVA or Gemma3 via Ollama). \\

Result logging & Logs the generated answer, the context used, and its type back into the MongoDB database. \\
\bottomrule
\end{tabularx}
\end{table}

For a better visualization of how the components interact with each other, Figure~\ref{fig:multimodal_pipeline} presents a flowchart illustrating the overall logic of the framework. 


\begin{figure}[H]
\centering
\begin{tikzpicture}[node distance=1.3cm and 2cm]

\node (db) [startend, text width=6cm, align=center] {\textbf{MongoDB}\\\textit{Question (text, options, image)}};

\node (preprocess) [process, below=of db, text width=6cm, align=center] {\textbf{Preprocessing} \\\textit{Normalization and Image Validation}};
\node (contains) [decision, below=of preprocess] {Contains image?};

\node (yolo) [process, right=2cm of contains, align=center] {\textbf{YOLOv8}\\  \textit{Sign Detection}};

\node (signs) [process, below=2.45cm of yolo, align=center] {\textbf{ChromaDB}\\ \textit{Sign Definitions} };

\node (rag) [process, below=2cm of contains, align=center] {\textbf{RAG-like Retrieval} \\ \textit{Text and Image Encodings}};

\node (llm) [startend, below=of rag, align=center] {\textbf{LLM (LLaVA / Gemma3)}\\ \textit{via Ollama}};

\node (save) [process, below=of llm, align=center] {\textbf{Result}\\ \textit{(answers, context, context\_type)}};

\draw [arrow] (db.south) -- (preprocess.north);

\draw [arrow] (preprocess.south) -- (contains.north);
\draw [arrow] (contains) -- node[above] {Yes} (yolo);
\draw [arrow] (yolo.south) -- (signs.north);
\draw [arrow] (signs.west) -- (rag.east);
\draw [arrow] (contains) -- node[left] {No} (rag);
\draw [arrow] (rag.south) -- (llm.north);
\draw [arrow] (llm.south) -- (save.north);
\draw [arrow] (save.east) -- ++(5.5,0) |-  (db.east);

\end{tikzpicture}
\caption{Multimodal question processing pipeline}
\label{fig:multimodal_pipeline}
\end{figure}




\section{Textual context extraction with RAG}
In order to support the automated generation process for the LLMs’ responses, the framework integrates a Retrieval-Augmented Generation method that has the purpose to extract automatically the articles that are the most similar in semantic meaning with the question, alongside with the possible choices. 

 

\subsection{Semantic Embedding}


 

Both the questions (text concatenated with answer options) and the documents from the auxiliary corpus (road safety legislation and traffic signs’ definitions) are transformed into semantic vectors using the all-MiniLM-L6-v2 model from sentence-transformers library. These vectors encode information and allow comparison between components based on cosine similarity \citep{delftstack_cosine}. This method is used for both the initial indexing of law articles and for the contextual search during testing. Indexing is done by ChromaDB in two collections: one containing law articles segmented into different paragraphs, and another one containing additional information in regard to the traffic signs found with YOLOv8. 
\subsection{Reranking}


For each question, semantic embedding is calculated and used to query the article collection, from which the closest 200 documents are selected based on cosine similarity. In order for these to be as relevant as possible, a CrossEncoder is also applied, through the cross-encoder/ms-macro-MiniLM-L6-v2 model, which reevaluates the question-context pairings and classifies them based on a semantic score. Documents below the threshold of 2.5 are eliminated, the ones above 5 are considered useful and a maximum of 10 are chosen in descending order, and if there are no articles found above 5, the best 3, or fewer if there are less than 3, between 2.5 and 5 are selected, again in descending order. This selective procedure helps narrow and enrich the context that is later fed into the LLM. 
\subsection{Preparing the context for the LLM model}

All articles found as context by going through the steps described at 3.3.1 and 3.3.2 are concatenated in a large text block that is introduced in the prompt as the RAG context. If the question also comes with an image, then the definitions that come from the visual detection will be added to the textual context found earlier and together they represent the full context part of the prompt that will be sent to the analyzed large language model. 

 
\section{Visual recognition with YOLOv8}

For the questions containing images, the system includes a visual recognition component that has the purpose of identifying the road signs included in the image for a better transmitted context. The detection is done with the help of YOLOv8 (You Only Look Once version 8), a one-stage object detection model known for its high performance and accuracy. This model has been pretrained on a personalized set of images with traffic signs, seen from different perspectives, difficult angles, from far afar, seen up close, all of this to help the model differentiate the signs as correctly as possible. 

The image dataset was made using the platform Make Sense AI \citep{makesense}, where I tagged road signs in the pictures with the corresponding class, which have the same name. This platform automatically makes labels, so the model knows what traffic signs can be seen and where they are placed in a picture. In Table~\ref{tab:yolo-bbox-example} is a representation of how this works. 




\begin{table}[H]
\centering
\caption{\textit{YOLOv8 Labeling Output and Corresponding Detection Image.} 
The image below was processed with YOLOv8, and the detected traffic signs are labeled using normalized coordinates.
Each label follows the format: \texttt{class\_id $x_{center}$ $y_{center}$ width height}.}
\label{tab:yolo-bbox-example}
\vspace{2mm}

\includegraphics[width=0.65\textwidth]{pics/000.jpg}
\vspace{1mm}

\textit{Figure: YOLOv8 detection on real-world traffic signs}
\vspace{3mm}

\small
\renewcommand{\arraystretch}{1.2}
\begin{tabularx}{\textwidth}{c l c c c c}
\toprule
\textbf{Class ID} & \textbf{Traffic Sign} & $x_{center}$ & $y_{center}$ & Width & Height \\
\midrule
43  & Cedează trecerea       & 0.599318 & 0.130870 & 0.161364 & 0.249301 \\
0   & Obligatoriu la dreapta & 0.607273 & 0.552273 & 0.131818 & 0.193007 \\
112 & Acces interzis         & 0.609545 & 0.351224 & 0.145455 & 0.176923 \\
\bottomrule
\end{tabularx}
\end{table}




For the training of the YOLOv8 model were used 5719 different images, and 365 for the evaluation. The ratio between training and evaluation was made to be 90\%-10\%. It has been trained with 100 epochs with this dataset for 242 detectable classes. Figure~\ref{fig:yolo-train-samples} shows some pictures used for the training. 


\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{pics/sample_images_grid.png}
\caption{\textit{Sample Images from YOLOv8 Training Set}}
\label{fig:yolo-train-samples}
\end{figure}



\section{Prompting }


After extracting the relevant context, this framework builds a complete prompt, adapted to the requirements of any question from the database, and sends it to a large language model to generate an automatic response with only the letters of the correct options considered. The prompt is made out of sections, each having its particular role essential in the question understanding and in finding the correct answer(s). A prompt ilustration can be seen in Tabel~\ref{tab:prompt}. 




\begin{table}[H]
\centering
\caption{\textit{Complete Prompt Instructions Used for LLM Inference (in Romanian)}}
\label{tab:prompt}
\begin{tabularx}{\textwidth}{@{}l X@{}}
\toprule
\textbf{Prompt Type} & \textbf{Full Prompt Text} \\
\midrule
Without context &
\texttt{Întrebare: \{intrebare['text']\}} \newline
\texttt{Opțiuni: \{optiuni\_formatate\}} \newline

Instrucțiuni: Răspunde DOAR cu literele mari corespunzătoare opțiunilor corecte, fără explicații. \newline
Selectează doar opțiunile corecte, în ordine alfabetică, fără a repeta literele. \newline
Formatul răspunsului trebuie să fie exact: [``A``], [``B``], [``C``], [``A``, ``B``], [``A``, ``C``], [``B``, ``C``], [``A``, ``B``, ``C``]. \\

With context &
\texttt{Întrebare: \{intrebare['text']\}} \newline
\texttt{Opțiuni: \{optiuni\_formatate\}} \newline
\texttt{Context: \{context\}} \newline

Instrucțiuni: Bazându-te pe contextul de mai sus, răspunde DOAR cu literele opțiunilor corecte, în ordine alfabetică. \newline
Selectează doar opțiunile corecte, în ordine alfabetică, fără a repeta literele. \newline
Formatul răspunsului trebuie să fie exact: [``A``], [``B``], [``C``], [``A``, ``B``], [``A``, ``C``], [``B``, ``C``], [``A``, ``B``, ``C``]. \\
\bottomrule
\end{tabularx}
\end{table}



The prompt used has a simple and clear form. The question is in the first row, followed by the options, concatenated so they are all on the same row, extracted context, and after are the instructions. It is mentioned that the answers should have letters in alphabetical order, and all possibilities for the answer are explicitly stated. This formula appeared to be the most efficient in testing. After some tries this became the standardized prompt utilized in evaluation due to the best results. In the prompt construction stage, the study made by \citet{pezeshkpour2023large} was also taken into account. This study shows that LLMs can be sensible when it comes to multiple-choice questions and the order of the options. Their results show significant variations in the response accuracy, depending on the position of the correct answer, even in identical prompting conditions. In order to mitigate this effect, the order of the options is identical to the one G.D.D.L.R. website from which the questions were scraped. 

 
\section{Tested LLMs and motivation for their choice}
The built prompt is sent to an LLM type via the local API provided by Ollama. The framework provides testing and comparison between models, and in this paper LLaVA:34B and Gemma3:27B will be analyzed. 

 

Communication with Ollama is done through HTTP POST requests to the dedicated endpoint /api/generate with the parameters sent in the payload: model (name of the used LLM, such as LLaVA:34B, Gemma3:27B), prompt (containing the question with options, context and instructions) and Images (the base64 encoding of the image if it exists). The securitized access is done with an authentication mechanism based on a JSON Web Token (JWT). This token is transmitted in the header of every request and validated by the Ollama server to allow access only to authorized users. 

 

When it comes to the inference component in this framework, two large language models were selected. Both have support for textual and visual questions, so they were a good choice for this study.  

 

LLaVA was selected for the visual part, being a known model for its performance in open-ended visual interpretation tasks. In its original paper \citep{liu2023visual}, LLaVA achieves competitive results on benchmarks such as VQAv2, ScienceQA and VizWis, making it comparable to closed source models like GPT-4V. 

 

On the other hand, Gemma3 was introduced in this research as a recent multimodal model, that combines a visual SigLIP encoder with a linguistic backbone optimized for instruction inference. Based on the official technical report \citep{team2025gemma}, Gemma3 is capable of image processing, supports contexts up to 128K and is almost comparable in performance with Gemini-1.5Pro.  

 

This selection was made in order to analyze the difference in efficiency between the two models based on the question type (having or not having an image attached) and to make a comparison in their two different paradigms in training and optimization. LLaVA is centered on visual fine-tuning with instructive data while Gemma3 is natively multimodally integrated within a scalable architecture. Using these models on the standardized G.D.D.L.R. questions dataset, an evaluation on how the legal and visual contexts are affecting accuracy will be made. 



%---------------------------
\chapter{Experiments and results}


This research is meant to evaluate how well LLMs answer G.D.D.L.R questions without context and how much the context extracted with RAG and visual context detected by YOLOv8 into the sign definitions help. With all this taken in consideration a discussion on which model performs better will be made. 
\section{Results comparison}
To evaluate the performance of LLMs in this multimodal framework, we will be looking at the results obtained after running both models (Gemma3:27B and LLaVA:34B). The study cases are divided into answers with or without context and with or without an image. A representation of how many correct and incorrect answers each model has given can be seen in Tabel~\ref{tab:answercomparison}. 


\begin{table}[H]
\centering
\caption{\textit{Correct vs. Incorrect Answers With and Without Context}}
\label{tab:answercomparison}
\vspace{1mm}
\begin{tabularx}{\textwidth}{@{}l l 
    >{\centering\arraybackslash}X 
    >{\centering\arraybackslash}X 
    >{\centering\arraybackslash}X 
    >{\centering\arraybackslash}X @{}}
\toprule
\textbf{Model} & \textbf{Question Type} & \textbf{Correct (no context)} & \textbf{Incorrect (no context)} & \textbf{Correct (context)} & \textbf{Incorrect (context)} \\
\midrule
Gemma3:27b & Without image & 426 & 401 & 532 & 295 \\
LLaVA:34b  & Without image & 380 & 447 & 423 & 404 \\
Gemma3:27b & With image    & 177 & 208 & 196 & 189 \\
LLaVA:34b  & With image    & 181 & 204 & 180 & 205 \\
\bottomrule
\end{tabularx}
\end{table}





In order to better understand the contribution of the context added, a heatmap was constructed for the four scenarios and can be seen in Figure~\ref{fig:heatmap-matrix}. It shows a clear visualization of how context affected each model. Gemma3:27B benefited from added textual context in a large number of cases for questions that don’t include a picture as seen in the bottom left cell, more than LLaVA:34B did. On the other hand, LLaVA:34B failed to improve its results in the G.D.D.L.R questions with images. 




\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{pics/final_confusion_matrix_updated.png}
\caption{\textit{Contextual confusion matrices showing the effect of added context on each model and question type. The bottom-left cell in each matrix reflects questions that were corrected by context.}}
\label{fig:heatmap-matrix}
\end{figure}





Table~\ref{tab:model-metrics} presents a comparative overview of the main performance metrics obtained by both models. It contains the percentages for correct answer with and without context, the proportion of cases where the context helped and harmed the answer, and a recall value calculated to see how many wrong answered questions without the context are corrected by adding context.

\begin{table}[H]
\centering
\caption{\textit{Model Evaluation Metrics Across Scenarios}}
\label{tab:model-metrics}
\begin{tabularx}{\textwidth}{@{}l 
    >{\centering\arraybackslash}X 
    >{\centering\arraybackslash}X 
    >{\centering\arraybackslash}X 
    >{\centering\arraybackslash}X 
    >{\centering\arraybackslash}X 
@{}}
\toprule
\textbf{Model} & \textbf{Accuracy with context} & \textbf{Accuracy without context} & \textbf{\% Helped by context} & \textbf{\% Harmed by context} & \textbf{Recall (strict)} \\
\midrule
Gemma3:27b (No image) & 0.64 & 0.52 & 0.16 & 0.03 & 0.33 \\
LLaVA:34b (No image)  & 0.51 & 0.46 & 0.10 & 0.04 & 0.18 \\
Gemma3:27b (With image) & 0.51 & 0.46 & 0.08 & 0.03 & 0.15 \\
LLaVA:34b (With image)  & 0.47 & 0.47 & 0.04 & 0.04 & 0.07 \\
\bottomrule
\end{tabularx}
\end{table}


\section{Experimental optimizations}
 

Going through the testing phase, there were made some adjustments on the prompting component and on the parameters used for the context extracted in order to increase the general performance of the framework 

 

On the prompting part, various variants were initially tested, including comprehensive and explicit explanations, but also summarized ones. The results on these prompts were inconsistent or generated invalid responses, like the same letter showing up twice in the response or the letter “D” appearing as response even though the options are A, B, C. 

The final form for the promt has a compact structure, so the role of each component is as clear as possible. This formula had the best results for the Gemma3 model in answering the first 100 questions as a metric for comparing results and it was then considered the standard in the evaluation and the comparison with LLaVA. 

 

For the RAG component, the first 200 articles were selected based on cosine similarity between the semantic embedding of the question and the documents saved in ChromaDB. Smaller numbers, like 50 or 100, were letting out some relevant articles in finding the correct answer to some analyzed sample questions, making the LLM give a wrong response. The top 200 provided sufficient coverage of relevant articles to be passed to CrossEncoder and to provide the best possible performance in the end. 

 

%---------------------------
\chapter{Discussion}

\section{Performance comparison}
In this section the performances for the two analyzed models, Gemma3:27B and LLaVA:34B, will be compared based on their capacity to correctly respond at the G.D.D.L.R. questions in 3 different scenarios presented: without context, with textual context using RAG, and with context extracted from both visual and textual sources. 

 

Looking at the questions without context, Gemma3:27B model had 603 (426 without images, and 177 with images) correct answers, and LLaVA:34B had less, precisely 561 (380 without images and 181 with images) correct answers. This shows that Gemma3 is more capable of understanding the questions and knowing the answer without any auxiliary information. 

 

Taking the questions with only textual RAG given context, Gemma3 has 532 correct answers, marking 106 more than without context. LLaVA has 423 in this case, also increasing the number of correct answers by 43 compared to the previous scenario. These questions show the fact that Gemma3 is using the context from the Romanian Road Safety Legislation better than its counterpart that is less influenced by it. 

 

In the last question subset, where the images are coming into consideration and the detection of traffic signs is analyzed with YOLOv8, Gemma3 increases its number of correct answers by 19 from 177 to 196, and on the other hand LLaVA lost one correct answer going from 181 to 180. These results indicate the fact that the road signs detection and their definitions introduced in the context don't bring a strong contribution to the final accuracy of the framework. Most probably causing this phenomenon is due to many pictures that don’t have any traffic signs in them to be detected, and they are asking other things like what a driver should do in a complicated drawn situation. There are also questions with images from a driver’s perspective, and they do not involve road signs. The YOLOv8 model is not trained for this kind of question and it’s normal for it to give a wrong answer. Some examples of questions with pictures that confuse the LLMs can be seen below in Tabel~\ref{tab:problematicquestions}.  


\begin{table}[H]
\centering
\caption{\textit{Examples of Multiple-Choice Questions Used in Evaluation}}
\label{tab:problematicquestions}
\renewcommand{\arraystretch}{1.2}
\small
\begin{tabularx}{\textwidth}{|X|X|X|}
\hline
\textbf{Question 1} & \textbf{Question 2} & \textbf{Question 3} \\
\hline

\begin{flushleft}
\textbf{Text:} Când ninge abundent veți folosi? \\
\textbf{A:} luminile de poziție \\
\textbf{B:} claxonul \\
\textbf{C:} luminile de întâlnire ale farurilor \\
\textbf{Gemma3:27b answer with context:} C \\
\textbf{LLaVA:34b answer with context:} C \\
\textbf{Correct:} C
\end{flushleft}
&

\begin{flushleft}
\textbf{Text:} Execută corect autoturismul manevra de depășire? \\
\textbf{A:} nu, deoarece autobuzul are prioritate la plecarea din stație \\
\textbf{B:} nu, deoarece această manevră nu este permisă în dreptul stațiilor mijloacelor de transport public \\
\textbf{C:} da, manevra este regulamentară \\
\textbf{Gemma3:27b answer with context:} B \\
\textbf{LLaVA:34b answer with context:} A \\
\textbf{Correct:} C
\end{flushleft}
&

\begin{flushleft}
\textbf{Text:} În ce ordine vor trece prin intersecție autoturismele la culoarea galbenă intermitentă a semaforului? \\
\textbf{A:} roșu, verde, albastru \\
\textbf{B:} roșu, albastru, verde \\
\textbf{C:} verde, albastru, roșu \\
\textbf{Gemma3:27b answer with context:} A, B, C \\
\textbf{LLaVA:34b answer with context:} A \\
\textbf{Correct:} C
\end{flushleft}
\\
\hline

\begin{center}
\includegraphics[width=0.9\linewidth]{pics/663.jpeg}
\end{center}
&
\begin{center}
\includegraphics[width=0.9\linewidth]{pics/845.jpeg}
\end{center}
&
\begin{center}
\includegraphics[width=0.9\linewidth]{pics/902.jpeg}
\end{center}
\\
\hline
\end{tabularx}
\end{table}



\section{Limitations}
Following the experimental evaluation, some limitations of the framework can be noted. One issue is context overload: in some cases, too long or imprecise context causes the model to generate wrong answers. This limitation was more often observed for the LLaVA model. Another challenge was visual context ambiguity. YOLOv8, while being a powerful model, was not optimally trained on this dataset. Given the 242 object classes, YOLOv8 would have learned more from more training images and longer training durations. In the current state, some misinterpretations and overlooks can be observed. 

Further limitations involve prompting sensibility. LLMs have different responses based on the order in prompt components or on how the instructions are written, so it’s not guaranteed that the optimal prompt for Gemma3 is also the best for LLaVA. Additionally, the Romanian traffic regulations do not provide enough information to answer the questions accurately. The documentation consists of articles and laws written in a juridic manner, difficult for making direct correlations with the questions that are written in a more colloquial language. Many questions are about practical situations or require car mechanics and signalization knowledge that is not in law articles and can be found in guides and teaching materials. All of this is affecting RAG efficiency because there are some cases in which there is not a single article relevant to the question and if the model doesn’t know the answer without context, it won’t know it with context either. Another possibility is to extract articles that are confusing the LLM when an article is over the threshold but has nothing to do with the question. 

Finally, there are limitations from zero-shot inference. The models in this research have been used without any specific example or prior training for the G.D.D.L.R. question format. They are answering only based on the given context from RAG and YOLOv8.

%---------------------------
\chapter{Conclusions and Future Work}

\section{Future Work}
 

The proposed framework could support further performance enhancements by considering possible improvements like fine-tuning the current model, experimenting with other visual detection models, or a better organized textual corpus. 

 

Fine-tuning on the G.D.D.L.R. dataset can be used for better learning the logic. Introducing questions and answers in the prompt as examples and classifying questions by kind of context (eg. Mechanical Knowledge, Traffic Signs Recognition, Traffic Signals, Traffic Legislation, etc.) can help build the context and guide the LLM to give better responses. Adding more explanations from the driving school courses in the article corpus could also make the context fit to cover a wider range of questions. 

 

The visual detection part could be improved by employing a larger model like YOLOv8m, YOLOv8l or DETR, trained on a bigger set of images with road signs.

 

Lastly, extending the framework to offer explanations for the answers provided could significantly improve the learning process of the users. 
\section{Conclusions}
This thesis proposed and evaluated an automated multimodal framework for answering G.D.D.L.R. driving license exam questions, based on integrating natural language processing (NLP), computer vision (CV), contextual augmentation (RAG) and LLM inference. 

 

By comparing two large language models, Gemma3:27B and LLaVA:34b, the results prove that adding textual context significantly improves the performance of the model. Gemma3 performed better in all 3 scenarios implemented: without context, with textual context using RAG, and with context extracted from both visual and textual sources. 

 

While adding visual corelations with YOLOv8 and definitions as context brings a visibly improved model, the most significant advantage was brought by the interpretation of the textual context using RAG. Further improvement could be made by enhancing training or experimenting with other models for visual detection. 

 

To conclude, the results attest the viability of the automated multimodal framework, while leaving space for future performance improvements with adjustments to the contextual corpus. 
 
% Bibliography / References.
\renewcommand\bibname{References}
\clearpage\phantomsection\addcontentsline{toc}{chapter}{\bibname}
\bibliographystyle{apacite}
\bibliography{bibliography}

\end{document}
