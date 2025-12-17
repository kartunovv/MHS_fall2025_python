FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        texlive-latex-base \
        texlive-latex-extra \
        texlive-fonts-recommended \
        latexmk \
        lmodern \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -e .

RUN mkdir -p artifacts

RUN python examples/generate_document.py && \
    pdflatex -output-directory=artifacts artifacts/document.tex && \
    mv artifacts/document.pdf artifacts/result.pdf

CMD ["ls", "-l", "artifacts"]
