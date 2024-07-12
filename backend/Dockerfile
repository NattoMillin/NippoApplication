FROM python:3
ENV PYTHONUNBUFFERED 1

# 環境変数を指定
ARG USERNAME
ARG GROUPNAME
ARG UID
ARG GID

# django-admin start appのpathが通っていないため、追加。
ENV PATH $PATH:/home/dev/.local

RUN mkdir /home/${USERNAME} && \
    mkdir /home/${USERNAME}/backend
WORKDIR /home/${USERNAME}/backend

# ユーザー作成
RUN groupadd -g ${GID} ${GROUPNAME} && \
    useradd -l -m -s /bin/bash -u ${UID} -g ${GID} ${USERNAME}

# 権限を保持した状態でコピー
COPY --chown=${USERNAME}:${GROUPNAME} backend/djangoprojects/requirements.txt /home/${USERNAME}/backend
RUN pip install --upgrade --no-cache-dir pip

# permission関係
RUN chown ${UID}:${GID} /home/${USERNAME} && \
    chmod 777 /home/${USERNAME}
    
USER ${USERNAME}
