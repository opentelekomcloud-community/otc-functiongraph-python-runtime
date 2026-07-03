# syntax=docker/dockerfile:1.7
FROM python:3.10-slim@sha256:5f9928ea39771e8ddf4fb9a96ab24f65f087793635614405a1dc9384f040852e

ENV HOME=/home/paas_user
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV GROUP_ID=1003
ENV GROUP_NAME=paas_user

ENV USER_ID=1003
ENV USER_NAME=paas_user

# Set timezone to UTC
ENV TZ=Etc/UTC

ENV IS_DOCKER_CONTAINER=1

RUN groupadd -g ${GROUP_ID} ${GROUP_NAME} && \
    useradd -u ${USER_ID} -g ${GROUP_ID} ${USER_NAME} && \
    mkdir -p ${HOME} && \
    chown ${USER_ID}:${GROUP_ID} ${HOME} && \
    chmod 750 ${HOME}

# Copy requirements.txt
COPY --chown=${USER_ID}:${GROUP_ID} ./requirements.txt ${HOME}/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-compile -r ${HOME}/requirements.txt

# Copy application files after dependencies for better layer caching.
COPY --chown=${USER_ID}:${GROUP_ID} ./src ${HOME}/src
COPY --chown=${USER_ID}:${GROUP_ID} ./entrypoint.sh ${HOME}/entrypoint.sh

RUN chmod 755 ${HOME}/entrypoint.sh

USER ${USER_NAME}
WORKDIR ${HOME}
EXPOSE 8000

ENTRYPOINT ["sh", "/home/paas_user/entrypoint.sh"]
