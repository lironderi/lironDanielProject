FROM python:3.9
COPY . /app
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP main.py
COPY ./app .
ENV PORT 5000
EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0" ]