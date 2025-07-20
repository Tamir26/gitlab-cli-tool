FROM python:3.11-alpine
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY mobileye-home-assignment.py .

EXPOSE 5000 


ENTRYPOINT ["python", "mobileye-home-assignment.py"]
CMD ["-h"]