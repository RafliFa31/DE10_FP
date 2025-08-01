# Gunakan base image Python
FROM python:3.9-slim-buster

# Atur direktori kerja di dalam kontainer
WORKDIR /app

# Salin requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin aplikasi Streamlit
COPY . .

# Paparkan port yang digunakan Streamlit
EXPOSE 8501

# Jalankan aplikasi Streamlit saat kontainer dimulai
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
