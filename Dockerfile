FROM python:3.9
COPY . /app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP main.py
ENV FLASK_DEBUG 1
COPY . .
ENV PORT 5000
EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0" ]