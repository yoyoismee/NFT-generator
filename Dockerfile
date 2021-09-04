FROM python:3.7-slim
COPY server/* ./
COPY generator.py ./
RUN pip install -r requirement_web.txt
CMD streamlit run nft-generator-web.py --server.port 80