# Unstructured: Pre-Processing Tools for Unstructured Data

`unstructured` is an open-source library that helps you process various types of documents (PDFs, Word docs, HTML, images, etc.) into clean, structured data that's ready for Large Language Models (LLMs).

## Quick Start

## Docker Support

Make the docker image:

```bash
make docker_build
make docker_build_push
```

Execute the docker image:
```bash
docker run -p 8000:8000 unstructured-api
```

Example usage:

```bash
curl -X POST "http://localhost:8000/process-file" \
     -F "file=@example-docs/fake-doc.rtf"
{"elements":"My First Heading\n\nMy first paragraph.\n\nTable Example:\n\nColumn 1 Column 2 Row 1, Cell 1 Row 1, Cell 2 Row 2, Cell 1 Row 2, Cell 2"}%  
```

## Features

- Supports multiple document types (PDFs, Word docs, HTML, images, etc.)
- Automatic file type detection
- OCR support for images and scanned documents
- Modular design for easy integration
- Docker support for easy deployment
