ARG GOLANG_VERSION=1
ARG PYTHON_VERSION=3

FROM golang:$GOLANG_VERSION AS golang

FROM python:$PYTHON_VERSION


RUN pip install ansible cookiecutter

COPY --from=golang /usr/local/go /usr/local/go

ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH
RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"
WORKDIR /

COPY . /src

ENTRYPOINT ["/src/test/test.sh"]
