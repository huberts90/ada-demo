package main

import (
	"flag"
	"github.com/bitly/go-simplejson"
	"github.com/gorilla/mux"
	"go.uber.org/zap"
	"log"
	"net/http"
)

func main() {
	port := flag.String("port", "8000", "Listening HTTP port")
	flag.Parse()

	// Create a logger
	logger, err := zap.NewDevelopment()
	if err != nil {
		panic(err)
	}
	defer logger.Sync()

	srv := NewHttpServer(logger)
	err = srv.Serve(*port)
	if err != nil {
		logger.Fatal("Server failed", zap.Error(err))
	}
}

type HttpServer struct {
	logger *zap.Logger
	router *mux.Router
}

func NewHttpServer(logger *zap.Logger) *HttpServer {
	srv := &HttpServer{
		logger: logger,
		router: mux.NewRouter(),
	}

	srv.router.Path("/repos/{owner}/{repository}").Methods(http.MethodGet).HandlerFunc(srv.Handle)

	return srv
}

func (server *HttpServer) Serve(port string) error {
	server.logger.Info("Http server listening", zap.String("port", port))
	return http.ListenAndServe(":"+port, server.router)
}

func (server *HttpServer) Handle(w http.ResponseWriter, r *http.Request) {
	server.logger.Info(r.Method, zap.String("PATH", r.URL.Path))

	json := simplejson.New()
	json.Set("id", "80272654")
	json.Set("name", "link-scraper")
	json.Set("description", "Link scraper in Go")
	json.Set("clone_url", "https://github.com/huberts90/go-link-scraper.git")

	payload, err := json.MarshalJSON()
	if err != nil {
		log.Println(err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(payload)
}
