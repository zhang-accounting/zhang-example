FROM python:3.10.10-bullseye AS python-build
RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /project/
COPY . /project

# install dependencies and project into the local packages directory
WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable


# run stage
FROM python:3.10.10-bullseye AS demo-build

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=python-build /project/__pypackages__/3.10/lib /project/pkgs


RUN mkdir /data
COPY data /data

COPY . /project
WORKDIR /project
# set command/entrypoint, adapt to fit your needs
RUN python main.py  run > /data/main.zhang
RUN mv /project/data/attachments /data/attachments


FROM kilerd/zhang:snapshot
COPY --from=demo-build --chmod=444 /data /data

EXPOSE 8000
