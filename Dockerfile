FROM quay.io/unstructured-io/base-images:wolfi-base-latest as base

USER root

WORKDIR /app

# Copy required files
COPY ./requirements requirements/
COPY unstructured unstructured
COPY test_unstructured test_unstructured
COPY example-docs example-docs
COPY app.py app.py

# Install additional dependencies and set up environment
RUN chown -R notebook-user:notebook-user /app && \
  apk add font-ubuntu git && \
  fc-cache -fv && \
  ln -s /usr/bin/python3.11 /usr/bin/python3

USER notebook-user

# Install Python dependencies, including FastAPI and Uvicorn
RUN find requirements/ -type f -name "*.txt" -exec pip3.11 install --no-cache-dir --user -r '{}' ';' && \
  pip3.11 install --no-cache-dir --user fastapi uvicorn && \ 
  python3.11 -c "from unstructured.nlp.tokenize import download_nltk_packages; download_nltk_packages()" && \
  python3.11 -c "from unstructured.partition.model_init import initialize; initialize()" && \
  python3.11 -c "from unstructured_inference.models.tables import UnstructuredTableTransformerModel; model = UnstructuredTableTransformerModel(); model.initialize('microsoft/table-transformer-structure-recognition')"

# Set environment variables
ENV PATH="${PATH}:/home/notebook-user/.local/bin"
ENV TESSDATA_PREFIX=/usr/local/share/tessdata

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]