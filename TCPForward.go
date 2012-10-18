package main

import (
	"fmt"
	"log"
	"net"
	"time"
)

//read data from socket which is created by parent, and push the read out data input chan to let parent know
//if no data is read out after time out, push signal to quit chan to let parent know
type MyChan struct {
	Mychan chan string
}

var glo_Consumer map[string]MyChan

func consumerClient(connection net.Conn, timeout time.Duration) {
	b := make([]byte, 20)
	mychan := make(chan string)
	n, err := connection.Read(b)

	if n > 0 {
		mychanT := new(MyChan)
		mychanT.Mychan = mychan
		glo_Consumer[string(b)] = *mychanT
	}
	if err != nil {
		fmt.Println(err)
		return
	}
	for {
		msg := <-mychan
		n, err := connection.Write([]byte(msg))
		if n > 0 {
			continue
		}
		if err != nil {
			fmt.Println(err)
			return
		}
	}
}

func producerClient(connection net.Conn, timeout time.Duration, consumer_chan map[string]MyChan) {
	b := make([]byte, 20)
	n, err := connection.Read(b)
	var myid string

	if n > 0 {
		myid = string(b)
	}
	if err != nil {
		fmt.Println(err)
		return
	}
	chunk := make([]byte, 1024)
	for {
		n, err := connection.Read(chunk)
		if n > 0 {
			v, ok := consumer_chan[myid]
			if ok {
				v.Mychan <- string(chunk)
			}
			continue
		}
		if err != nil {
			fmt.Println(err)
			return
		}
	}
}

func main4Consumer() {
	ln, err := net.Listen("tcp", ":44444")
	if err != nil {
		log.Fatal(err)
		fmt.Println("found error in listen")
		return
	}
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Fatal(err)
			fmt.Println("found error in accept")
			continue
		}

		go consumerClient(conn, 20)
	}

}

func main() {
	glo_Consumer = make(map[string]MyChan)
	ln, err := net.Listen("tcp", ":44445")
	if err != nil {
		log.Fatal(err)
		fmt.Println("found error in listen")
		return
	}
	go main4Consumer()
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Fatal(err)
			fmt.Println("found error in accept")
			continue
		}

		go producerClient(conn, 20, glo_Consumer)
	}
}
