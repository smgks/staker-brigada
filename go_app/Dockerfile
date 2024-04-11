FROM golang:1.22.2-alpine3.19 as builder

WORKDIR /app

COPY . .

RUN go mod download

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

FROM alpine:latest

WORKDIR /root/

COPY --from=builder /main .

EXPOSE 8080

CMD ["./main"]
