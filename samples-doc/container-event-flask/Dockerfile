FROM python:3.10-slim

ENV HOME=/home/paas_user
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

ENV GROUP_ID=1003
ENV GROUP_NAME=paas_user

ENV USER_ID=1003
ENV USER_NAME=paas_user

# Set timezone to UTC
ENV TZ=Etc/UTC

RUN groupadd -g ${GROUP_ID} ${GROUP_NAME} && \
    useradd -u ${USER_ID} -g ${GROUP_ID} ${USER_NAME} && \
    mkdir -p ${HOME} && \
    chown ${USER_ID}:${GROUP_ID} ${HOME} && \
    chmod 750 ${HOME}

# Copy requirements.txt
COPY --chown=${USER_ID}:${GROUP_ID} ./requirements.txt ${HOME}/requirements.txt

RUN python -m pip install --no-compile -r ${HOME}/requirements.txt

# Copy application files after dependencies for better layer caching.
COPY --chown=${USER_ID}:${GROUP_ID} ./src ${HOME}/src
COPY --chown=${USER_ID}:${GROUP_ID} ./entrypoint.sh ${HOME}/entrypoint.sh

RUN chmod 755 ${HOME}/entrypoint.sh

USER ${USER_NAME}
WORKDIR ${HOME}
EXPOSE 8000

ENTRYPOINT ["sh", "/home/paas_user/entrypoint.sh"]
