# Gunakan image Python yang ringan
FROM python:3.12-slim

# Set working directory dalam container
WORKDIR /app

# Salin file ke container
COPY . /app/

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan aplikasi Flask
CMD ["python", "app.py"]