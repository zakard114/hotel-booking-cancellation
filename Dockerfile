FROM python:3.11-slim
# FROM: base image for every later layer.
# Purpose: a small image that already has Python 3.11.
# When: first line of the Dockerfile.

WORKDIR /app
# WORKDIR: set the in-container working directory to /app.
# Purpose: COPY, RUN, and CMD share one path.
# When: right after the base image, before any files are copied.

# libgomp is the OpenMP runtime XGBoost needs. Without it, import fails on slim.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# COPY requirements.txt: put the pin list at /app.
# Purpose: pip installs from this file, and this layer can cache before code changes.
# When: before source and model copies.

RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install: install the pinned packages inside the image.
# Purpose: pandas, scikit-learn, xgboost, and flask are present at runtime.
# When: immediately after the requirements copy.

COPY src/ ./src/
# COPY src/: prediction service code.
# Purpose: the container can run predict.py.
# When: after dependencies are installed.

COPY ui_dummy/ ./ui_dummy/
# COPY ui_dummy/: HoldRisk desk and Ops static files.
# Purpose: Flask serves / and /ui/* from this folder.
# When: right after src/ is copied.

COPY models/ ./models/
# COPY models/: trained artifact, including model.bin.
# Purpose: predict.py loads /app/models/model.bin at boot.
# When: same stage as the source copy. The model must exist at runtime.

EXPOSE 9696
# EXPOSE: document that the process listens on 9696.
# Purpose: the host maps that port with -p.
# When: after files and dependencies, before the start command.

CMD ["python", "src/predict.py"]
# CMD: default command when the container starts.
# Purpose: run the Flask server (it binds 0.0.0.0 and PORT, default 9696).
# When: last line. docker run executes this.
