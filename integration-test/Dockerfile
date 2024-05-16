FROM golang:1.21.10-alpine3.19 as dev
WORKDIR /usr/src/app

FROM dev as build
# Maximize docker caching by downloading our Go dependencies early
COPY go.mod go.sum ./
RUN go mod download
COPY . .

# Build mocks
FROM build as build-mocks
RUN go build -ldflags="${LDFLAGS} -w -s" -o /usr/local/bin/mock-github  cmd/mock-github/main.go
RUN go test -tags=integration -o /usr/local/bin/integration-tests -c cmd/integration-test/demo_test.go

FROM alpine:3.19.1 as deploy-mocks
WORKDIR /
COPY --from=build-mocks /usr/local/bin/mock-github /usr/local/bin/mock-github
COPY --from=build-mocks /usr/local/bin/integration-tests /usr/local/bin/integration-tests