//  ============LICENSE_START===============================================
//  Copyright (C) 2023 Nordix Foundation. All rights reserved.
//  ========================================================================
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//  ============LICENSE_END=================================================
//

package main

import (
	"bytes"
	"compress/gzip"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/http/pprof"
	"os"
	"os/signal"
	"runtime"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/gorilla/mux"
	jsoniter "github.com/json-iterator/go"
	log "github.com/sirupsen/logrus"
	"golang.org/x/oauth2/clientcredentials"
)

type JobDefinition struct {
	InfoTypeID    string `json:"info_type_id"`
	JobOwner      string `json:"job_owner"`
	StatusNotificationURI  string `json:"status_notification_uri"`
	JobDefinition struct {
		Filter           json.RawMessage `json:"filter"`
		DeliveryInfo     struct {
			Topic            string `json:"topic"`
			BootStrapServers string `json:"bootStrapServers"`
		} `json:"deliveryInfo"`
	} `json:"job_definition"`
}

const jobdef = "/config/jobDefinition.json"

var rapp_id = os.Getenv("APPID")

var rapp_ns = os.Getenv("APPNS")

var bootstrapserver = os.Getenv("KAFKA_SERVER")

var topic = os.Getenv("TOPIC")

var ics_server = os.Getenv("ICS")

var jwt_file = os.Getenv("JWT_FILE")

var ssl_path = os.Getenv("SSLPATH")

var gzipped_data = os.Getenv("GZIP")

var log_payload = os.Getenv("LOG_PAYLOAD")

// These are optional - if rapp is fethcing the token instead of the side car
var creds_grant_type = os.Getenv("CREDS_GRANT_TYPE")
var creds_client_secret = os.Getenv("CREDS_CLIENT_SECRET")
var creds_client_id = os.Getenv("CREDS_CLIENT_ID")
var creds_service_url = os.Getenv("AUTH_SERVICE_URL")

var gid = ""
var cid = "cid-0"

var msg_count int = 0
var msg_corrupted_count int = 0

var jobid = "<not-set>"
var consumer_type = "<not-set>"

var currentToken = ""

var appStatus = "INIT"

var msg_per_sec int = 0

var httpclient = &http.Client{}

// == Main ==//
func main() {

	log.SetLevel(log.InfoLevel)
	log.SetLevel(log.DebugLevel)

	log.Info("Server starting...")

	if creds_service_url != "" {
		log.Warn("Disabling jwt retrieval from side car")
		jwt_file = ""
	}

	if rapp_id == "" {
		log.Error("Env APPID not set")
		os.Exit(1)
	}

	if rapp_ns == "" {
		log.Error("Env APPNS not set")
		os.Exit(1)
	}

	if bootstrapserver == "" {
		log.Error("Env KAFKA_SERVER not set")
		os.Exit(1)
	}

	if topic == "" {
		log.Error("Env TOPIC not set")
		os.Exit(1)
	}

	if ics_server == "" {
		log.Error("Env ICS not set")
		os.Exit(1)
	}

	rtr := mux.NewRouter()
	rtr.HandleFunc("/statistics", statistics)
	rtr.HandleFunc("/status", status)
	rtr.HandleFunc("/logging/{level}", logging_level)
	rtr.HandleFunc("/logging", logging_level)
	rtr.HandleFunc("/", alive)

	//For perf/mem profiling
	rtr.HandleFunc("/custom_debug_path/profile", pprof.Profile)

	http.Handle("/", rtr)

	fileBytes, err := os.ReadFile(jobdef)
	if err != nil {
		log.Error("Cannot read job defintion file: ", jobdef, err)
		os.Exit(1)
	}
	fmt.Println("FROM FILE")
	fmt.Println(string(fileBytes))

	job_json := JobDefinition{}
	err = jsoniter.Unmarshal([]byte(fileBytes), &job_json)
	if err != nil {
		log.Error("Cannot parse job defintion file: ", jobdef, err)
		os.Exit(1)
	}
	job_type := job_json.InfoTypeID
	job_json.JobDefinition.DeliveryInfo.Topic = topic
	job_json.JobDefinition.DeliveryInfo.BootStrapServers = bootstrapserver

        gid = "pm-rapp-" + job_type + "-" + rapp_id

        jobid = "rapp-job-" + job_type + "-" + rapp_id

	json_bytes, err := json.Marshal(job_json)
	if err != nil {
		log.Error("Cannot marshal job json", err)
		os.Exit(1)
	}

	json_str := string(json_bytes)

	if strings.HasPrefix(bootstrapserver, "http://") {
		if creds_service_url != "" {
			consumer_type = "accesstoken strimzi bridge consumer"
			retrive_token_strimzi()
		}
	} else {
		go read_kafka_messages()
	}

	ok := false
	if ics_server != "" {
		for !ok {
			log.Debug("Registring job: ", jobid, " json: ", json_str)
			ok, _ = send_http_request([]byte(json_str), http.MethodPut, "http://"+ics_server+"/data-consumer/v1/info-jobs/"+jobid, "", currentToken, 0, false)
			if !ok {
				log.Info("Failed to register job: ", jobid, " - retrying")
				time.Sleep(time.Second)
			}
		}
	} else {
		log.Info("No job registered - read from topic only")
	}
	if strings.HasPrefix(bootstrapserver, "http://") {
		go read_bridge_messages()
	}

	go calc_average()

	http_port := "80"
	http_server := &http.Server{Addr: ":" + http_port, Handler: nil}

	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		fmt.Println("Setting handler for signal sigint and sigterm")
		sig := <-sigs
		appStatus = "TERMINATING"
		fmt.Printf("Received signal %s - application will terminate\n", sig)

		if strings.HasPrefix(bootstrapserver, "http://") {
			log.Debug("stopping strimzi consumer for job: ", jobid)
			ok, _ = send_http_request(nil, http.MethodDelete, bootstrapserver+"/consumers/"+gid+"/instances/"+cid, "", currentToken, 0, false)
			if !ok {
				log.Info("Failed to delete consumer "+cid+" in group: ", gid, " - retrying")
			}
		}

		ok := false
		if ics_server != "" {
			for !ok {
				log.Debug("stopping job: ", jobid, " json: ", json_str)
				ok, _ = send_http_request(nil, http.MethodDelete, "http://"+ics_server+"/data-consumer/v1/info-jobs/"+jobid, "", currentToken, 0, false)
				if !ok {
					log.Info("Failed to stop job: ", jobid, " - retrying")
					time.Sleep(time.Second)
				}
			}
		}
		http_server.Shutdown(context.Background())
	}()
	appStatus = "RUNNING"
	log.Info("Starting http service...")
	err = http_server.ListenAndServe()
	if err == http.ErrServerClosed { // graceful shutdown
		log.Info("http server shutdown...")
		os.Exit(1)
	} else if err != nil {
		log.Error("http server error: ", err)
		log.Info("http server shutdown...")
		os.Exit(1)
	}

	//Wait until all go routines has exited
	runtime.Goexit()

	log.Warn("main routine exit")
	log.Warn("server is stopping...")
}

// Simple alive check
func alive(w http.ResponseWriter, req *http.Request) {
	//Alive check
}

// Get/Set logging level
func logging_level(w http.ResponseWriter, req *http.Request) {
	vars := mux.Vars(req)
	if level, ok := vars["level"]; ok {
		if req.Method == http.MethodPut {
			switch level {
			case "trace":
				log.SetLevel(log.TraceLevel)
			case "debug":
				log.SetLevel(log.DebugLevel)
			case "info":
				log.SetLevel(log.InfoLevel)
			case "warn":
				log.SetLevel(log.WarnLevel)
			case "error":
				log.SetLevel(log.ErrorLevel)
			case "fatal":
				log.SetLevel(log.FatalLevel)
			case "panic":
				log.SetLevel(log.PanicLevel)
			default:
				w.WriteHeader(http.StatusNotFound)
			}
		} else {
			w.WriteHeader(http.StatusMethodNotAllowed)
		}
	} else {
		if req.Method == http.MethodGet {
			msg := "none"
			if log.IsLevelEnabled(log.PanicLevel) {
				msg = "panic"
			} else if log.IsLevelEnabled(log.FatalLevel) {
				msg = "fatal"
			} else if log.IsLevelEnabled(log.ErrorLevel) {
				msg = "error"
			} else if log.IsLevelEnabled(log.WarnLevel) {
				msg = "warn"
			} else if log.IsLevelEnabled(log.InfoLevel) {
				msg = "info"
			} else if log.IsLevelEnabled(log.DebugLevel) {
				msg = "debug"
			} else if log.IsLevelEnabled(log.TraceLevel) {
				msg = "trace"
			}
			w.Header().Set("Content-Type", "application/text")
			w.Write([]byte(msg))
		} else {
			w.WriteHeader(http.StatusMethodNotAllowed)
		}
	}
}

// Get app state
func status(w http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodGet {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	_, err := w.Write([]byte(appStatus))
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		log.Error("Cannot send statistics json")
		return
	}
}

// producer statictics, all jobs
func statistics(w http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodGet {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	m := make(map[string]interface{})
	log.Debug("rapp statictics")

	req.Header.Set("Content-Type", "application/json; charset=utf-8")
	m["number-of-messages"] = strconv.Itoa(msg_count)
	m["number-of-corrupted-messages"] = strconv.Itoa(msg_corrupted_count)
	m["job id"] = jobid
	m["group id"] = gid
	m["client id"] = cid
	m["kafka consumer type"] = consumer_type
	m["server"] = bootstrapserver
	m["topic"] = topic
	m["messages per sec"] = msg_per_sec

	json, err := json.Marshal(m)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		log.Error("Cannot marshal statistics json")
		return
	}
	_, err = w.Write(json)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		log.Error("Cannot send statistics json")
		return
	}
}

func calc_average() {

	for true {
		v := msg_count
		time.Sleep(60 * time.Second)
		msg_per_sec = (msg_count - v) / 60
	}
}

func send_http_request(jsonData []byte, method string, url string, contentType string, accessToken string, alt_ok_response int, returnJson bool) (bool, map[string]interface{}) {

	var req *http.Request
	var err error
	if jsonData != nil {
		req, err = http.NewRequest(method, url, bytes.NewBuffer(jsonData))
		if err != nil {
			log.Error("Cannot create http request method: ", method, " url: ", url)
			return false, nil
		}
		if contentType == "" {
			req.Header.Set("Content-Type", "application/json; charset=utf-8")
		} else {
			req.Header.Set("Content-Type", contentType)
		}
	} else {
		req, err = http.NewRequest(method, url, nil)
		if err != nil {
			log.Error("Cannot create http request method: ", method, " url: ", url)
			return false, nil
		}
	}
	if jwt_file != "" || creds_service_url != "" {
		if accessToken != "" {
			req.Header.Set("Authorization", "Bearer "+accessToken)
		} else {
			log.Error("Cannot create http request for url: ", url, " - token missing")
			return false, nil
		}
	}
	log.Debug("Http request: ", req)
	resp, err2 := httpclient.Do(req)
	if err2 != nil {
		log.Error("Cannot send http request, method: ", method, "url: ", url)
	} else {
		if resp.StatusCode == 200 || resp.StatusCode == 201 || resp.StatusCode == 204 {

			if returnJson {
				defer resp.Body.Close()
				body, err3 := ioutil.ReadAll(resp.Body)
				if err3 != nil {
					log.Error("Cannot read body, method: ", method, ", url: ", url, " resp: ", resp.StatusCode)
					return false, nil
				} else {
					var responseJson map[string]interface{}
					err := json.Unmarshal(body, &responseJson)
					if err != nil {
						log.Error("Received msg not json? - cannot unmarshal")
						return false, nil
					}
					fmt.Println(string(body))
					log.Debug("Accepted response code: ", resp.StatusCode)
					return true, responseJson
				}
			}

			log.Debug("Accepted response code: ", resp.StatusCode)
			return true, nil
		} else {
			if alt_ok_response != 0 && resp.StatusCode == alt_ok_response {

				if returnJson {
					defer resp.Body.Close()
					body, err3 := ioutil.ReadAll(resp.Body)
					if err3 != nil {
						log.Error("Cannot read body, method: ", method, ", url: ", url, " resp: ", resp.StatusCode)
						return false, nil
					} else {
						var responseJson map[string]interface{}
						err := json.Unmarshal(body, &responseJson)
						if err != nil {
							log.Error("Received msg not json? - cannot unmarshal")
							return false, nil
						}
						fmt.Println(string(body))
						log.Debug("Accepted alternative response code: ", resp.StatusCode)
						return true, responseJson
					}
				}
			} else {
				log.Error("Bad response, method: ", method, " url: ", url, " resp: ", resp.StatusCode, " resp: ", resp)
			}
		}
	}
	return false, nil

}

func retrive_token_strimzi() {
	log.Debug("Get token inline - strimzi comm")

	conf := &clientcredentials.Config{
		ClientID:     creds_client_id,
		ClientSecret: creds_client_secret,
		TokenURL:     creds_service_url,
	}
	var modExpiry = time.Now()
	ok := false
	for !ok {
		token, err := conf.Token(context.Background())
		if err != nil {
			log.Warning("Cannot fetch access token: ", err, " - retrying ")
			time.Sleep(time.Second)
			continue
		}
		log.Debug("token: ", token)
		log.Debug("TokenValue: ", token.AccessToken)
		log.Debug("Expiration: ", token.Expiry)
		modExpiry = token.Expiry.Add(-time.Minute)
		log.Debug("Modified expiration: ", modExpiry)
		currentToken = token.AccessToken
		ok = true
	}
	log.Debug("Initial token ok")
	diff := modExpiry.Sub(time.Now())
	go func() {
		select {
		case <-time.After(diff):
			for !ok {
				token, err := conf.Token(context.Background())
				if err != nil {
					log.Warning("Cannot fetch access token: ", err, " - retrying ")
					time.Sleep(time.Second)
					continue
				}
				log.Debug("token: ", token)
				log.Debug("TokenValue: ", token.AccessToken)
				log.Debug("Expiration: ", token.Expiry)
				modExpiry = token.Expiry.Add(-time.Minute)
				log.Debug("Modified expiration: ", modExpiry)
				currentToken = token.AccessToken
				ok = true
			}
			diff = modExpiry.Sub(time.Now())
		}
	}()
}

func retrive_token(c *kafka.Consumer) {
	log.Debug("Get token inline")
	conf := &clientcredentials.Config{
		ClientID:     creds_client_id,
		ClientSecret: creds_client_secret,
		TokenURL:     creds_service_url,
	}
	token, err := conf.Token(context.Background())
	if err != nil {
		log.Warning("Cannot fetch access token: ", err)
		c.SetOAuthBearerTokenFailure(err.Error())
		return
	}
	extensions := map[string]string{}
	log.Debug("token: ", token)
	log.Debug("TokenValue: ", token.AccessToken)
	log.Debug("Expiration: ", token.Expiry)
	t := token.Expiry.Add(-time.Minute)
	log.Debug("Modified expiration: ", t)
	oauthBearerToken := kafka.OAuthBearerToken{
		TokenValue: token.AccessToken,
		Expiration: t,
		Extensions: extensions,
	}
	log.Debug("Setting new token to consumer")
	setTokenError := c.SetOAuthBearerToken(oauthBearerToken)
	currentToken = token.AccessToken
	if setTokenError != nil {
		log.Warning("Cannot cannot set token in client: ", setTokenError)
		c.SetOAuthBearerTokenFailure(setTokenError.Error())
	}
}

func gzipWrite(w io.Writer, data *[]byte) error {
	gw, err1 := gzip.NewWriterLevel(w, gzip.BestSpeed)

	if err1 != nil {
		return err1
	}
	defer gw.Close()
	_, err2 := gw.Write(*data)
	return err2
}

func read_bridge_messages() {

	consumer_type = "unsecure strimzi bridge consumer"
	if creds_service_url != "" {
		consumer_type = "accesstoken strimzi bridge consumer"
	}
	ok := false
	log.Debug("Cleaning consumer "+cid+" in group: ", gid)
	ok, _ = send_http_request(nil, http.MethodDelete, bootstrapserver+"/consumers/"+gid+"/instances/"+cid, "", currentToken, 0, false)
	if !ok {
		log.Info("Failed to delete consumer "+cid+" in group: ", gid, " - it may not exist - ok")
	}
	var bridge_base_url = ""
	ok = false
	json_str := "{\"name\": \"" + cid + "\", \"auto.offset.reset\": \"latest\",\"format\": \"json\"}"
	for !ok {
		log.Debug("Creating consumer "+cid+" in group: ", gid)
		var respJson map[string]interface{}
		ok, respJson = send_http_request([]byte(json_str), http.MethodPost, bootstrapserver+"/consumers/"+gid, "application/vnd.kafka.v2+json", currentToken, 409, true) //409 if consumer already exists
		if ok {
			bridge_base_url = fmt.Sprintf("%s", respJson["base_uri"])
		} else {
			log.Info("Failed create consumer "+cid+" in group: ", gid, " - retrying")
			time.Sleep(time.Second)
		}
	}

	ok = false
	json_str = "{\"topics\": [\"" + topic + "\"]}"

	for !ok {
		log.Debug("Subscribing to topic: ", topic)
		ok, _ = send_http_request([]byte(json_str), http.MethodPost, bridge_base_url+"/subscription", "application/vnd.kafka.v2+json", currentToken, 0, false)
		if !ok {
			log.Info("Failed subscribe to topic: ", topic, " - retrying")
			time.Sleep(time.Second)
		}
	}

	for true {
		log.Debug("Reading messages on topic: ", topic)

		var req *http.Request
		var err error
		url := bridge_base_url + "/records"

		req, err = http.NewRequest(http.MethodGet, url, nil)
		if err != nil {
			log.Error("Cannot create http request method: GET, url: ", url)
			time.Sleep(1 * time.Second)
			continue
		}
		req.Header.Set("accept", "application/vnd.kafka.json.v2+json")

		if creds_service_url != "" {
			if currentToken != "" {
				req.Header.Add("authorization", currentToken)
			} else {
				log.Error("Cannot create http request for url: ", url, " - token missing")
				time.Sleep(1 * time.Second)
				continue
			}
		}

		values := req.URL.Query()
		values.Add("timeout", "10000")
		req.URL.RawQuery = values.Encode()

		log.Debug(req)

		resp, err2 := httpclient.Do(req)
		if err2 != nil {
			log.Error("Cannot send http request, method: GET, url: ", url)
			time.Sleep(1 * time.Second)
			continue
		} else {
			body, err := ioutil.ReadAll(resp.Body)
			resp.Body.Close()
			if resp.StatusCode == 200 || resp.StatusCode == 201 || resp.StatusCode == 204 {
				log.Debug("Accepted response code: ", resp.StatusCode)

				if err != nil {
					log.Error("Cannot read body, method: GET, url: ", url, " resp: ", resp.StatusCode)
				} else {
					var responseJson []interface{}
					err := json.Unmarshal(body, &responseJson)
					if err != nil {
						log.Error("Received msg not json? - cannot unmarshal")
						msg_corrupted_count++
					} else {
						if len(responseJson) == 0 {
							log.Debug("No message")
							continue
						}
						for _, item := range responseJson {
							j, err := json.MarshalIndent(item, "", " ")
							if err != nil {
								log.Error("Message in array not json? - cannot unmarshal")
								msg_corrupted_count++
							} else {
								msg_count++
								if log_payload != "" {
									fmt.Println("Message: " + string(j))
								}
							}
						}
					}
				}

				log.Debug("Commiting message")
				ok, _ = send_http_request(nil, http.MethodPost, bridge_base_url+"/offsets", "", currentToken, 0, false)
				if !ok {
					log.Info("Failed to commit message")
				}

			} else {
				log.Error("Bad response, method: GET, url: ", url, " resp: ", resp.StatusCode)
				log.Error("Bad response, data: ", string(body))
			}
		}
	}

}

func read_kafka_messages() {
	var c *kafka.Consumer = nil
	log.Info("Creating kafka consumer...")
	var err error
	for c == nil {
		if jwt_file == "" && creds_service_url == "" {
			if ssl_path == "" {
				log.Info("unsecure consumer")
				consumer_type = "kafka unsecure consumer"
				c, err = kafka.NewConsumer(&kafka.ConfigMap{
					"bootstrap.servers": bootstrapserver,
					"group.id":          gid,
					"client.id":         cid,
					"auto.offset.reset": "latest",
				})
			} else {
				log.Info("ssl consumer")
				consumer_type = "kafka ssl consumer"
				c, err = kafka.NewConsumer(&kafka.ConfigMap{
					"bootstrap.servers":        bootstrapserver,
					"group.id":                 gid,
					"client.id":                cid,
					"auto.offset.reset":        "latest",
					"security.protocol":        "SSL",
					"ssl.key.location":         ssl_path + "/clt.key",
					"ssl.certificate.location": ssl_path + "/clt.crt",
					"ssl.ca.location":          ssl_path + "/ca.crt",
				})
			}
		} else {
			if ssl_path != "" {
				panic("SSL cannot be configued with JWT_FILE or RAPP_AUTH_SERVICE_URL")
			}
			log.Info("sasl consumer")
			consumer_type = "kafka sasl unsecure consumer"
			c, err = kafka.NewConsumer(&kafka.ConfigMap{
				"bootstrap.servers": bootstrapserver,
				"group.id":          gid,
				"client.id":         cid,
				"auto.offset.reset": "latest",
				"sasl.mechanism":    "OAUTHBEARER",
				"security.protocol": "SASL_PLAINTEXT",
			})
		}
		if err != nil {
			log.Warning("Cannot create kafka consumer - retrying, error: ", err)
			time.Sleep(1 * time.Second)
		}
	}

	log.Info("Creating kafka consumer - ok")
	log.Info("Start subscribing to topic: ", topic)
	topic_ok := false
	for !topic_ok {
		err = c.SubscribeTopics([]string{topic}, nil)
		if err != nil {
			log.Info("Topic reader cannot start subscribing on topic: ", topic, " - retrying --  error details: ", err)
		} else {
			log.Info("Topic reader subscribing on topic: ", topic)
			topic_ok = true
		}
	}

	fileModTime := time.Now()
	for {
		if jwt_file != "" {
			fileInfo, err := os.Stat(jwt_file)
			if err == nil {
				if fileModTime != fileInfo.ModTime() {
					log.Debug("JWT file is updated")
					fileModTime = fileInfo.ModTime()
					fileBytes, err := ioutil.ReadFile(jwt_file)
					if err != nil {
						log.Error("JWT file read error: ", err)
					} else {
						fileString := string(fileBytes)
						log.Info("JWT: ", fileString)
						t := time.Now()
						t15 := time.Second * 300
						t = t.Add(t15)
						oauthBearerToken := kafka.OAuthBearerToken{
							TokenValue: fileString,
							Expiration: t,
						}
						log.Debug("Setting new token to consumer")
						setTokenError := c.SetOAuthBearerToken(oauthBearerToken)
						if setTokenError != nil {
							log.Warning("Cannot cannot set token in client: ", setTokenError)
						}
					}
				} else {
					log.Debug("JWT file not updated - OK")
				}
			} else {
				log.Error("JWT does not exist: ", err)
			}
		}
		ev := c.Poll(1000)
		if ev == nil {
			log.Debug(" Nothing to consume on topic: ", topic)
			continue
		}
		switch e := ev.(type) {
		case *kafka.Message:
			var pdata *[]byte = &e.Value
			if gzipped_data != "" {
				var buf bytes.Buffer
				err = gzipWrite(&buf, pdata)
				if err != nil {
					log.Warning("Cannot unzip data")
					pdata = nil
				} else {
					*pdata = buf.Bytes()
					fmt.Println("Unzipped data")
				}
			}
			if pdata != nil {
				buf := &bytes.Buffer{}

				if err := json.Indent(buf, *pdata, "", " "); err != nil {
					log.Warning("Received msg not json?")
				} else {
					fmt.Println(buf.String())
					msg_count++
					fmt.Println("Number of received json msgs: " + strconv.Itoa(msg_count))
				}
			}
			c.Commit()
		case kafka.Error:
			fmt.Fprintf(os.Stderr, "%% Error: %v: %v\n", e.Code(), e)

		case kafka.OAuthBearerTokenRefresh:
			if jwt_file == "" {
				oart, ok := ev.(kafka.OAuthBearerTokenRefresh)
				fmt.Println(oart)
				if !ok {
					continue
				}
				retrive_token(c)
			}
		default:
			fmt.Printf("Ignored %v\n", e)
		}

	}
}
