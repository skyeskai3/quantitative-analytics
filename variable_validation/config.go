package main

import "redacted/for/proprietary/reasons/idb" //note this is not a real package

type Config struct {
	Pair string     `json:"pair"`
	DB   idb.Config `json:"db"`
}
