package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"time"

	"redacted/for/proprietary/reasons/helper" //note this is not a real package
	"redacted/for/proprietary/reasons/idb"    //note this is not a real package
)

var (
	cfgFile string
)

func main() {
	flag.StringVar(&cfgFile, "config", "", "the config file")
	flag.StringVar(&cfgFile, "c", "", "the config file")
	flag.Parse()

	if cfgFile == "" {
		flag.PrintDefaults()
		// mattermost.MsgProd("error no config passed")
		os.Exit(1)
	}
	cfg, err := helper.LoadConfig[Config](cfgFile)
	if err != nil {
		// mattermost.MsgProd("could not load config file - " + err.Error())
		log.Fatal("unable to load config file")
	}

	currentYear := time.Now().Year()

	// All vars being passed for AI integration
	variables := []string{"var1", "var2", "var3", "var4", "var5", "var6", "var7", "var8", "var9", "var10", "var11", "var12", "var13", "var14", "var15", "var16", "var17", "var18", "var19", "var20"}

	db := idb.New(cfg.DB)

	for _, variable := range variables {
		sqlQuery := fmt.Sprintf(`
			SELECT YEAR(notified), MIN(%s), MAX(%s)
			FROM table1
			WHERE pair=? AND YEAR(notified)>=2014 AND YEAR(notified)<?
			GROUP BY YEAR(notified)
			ORDER BY YEAR(notified)
			LIMIT 20
		`, variable, variable)

		rows, err := db.Query(sqlQuery, cfg.Pair, currentYear+1)
		if err != nil {
			log.Fatal(err)
		}
		defer rows.Close()

		for rows.Next() {
			var year int
			var minVal, maxVal float64
			if err := rows.Scan(&year, &minVal, &maxVal); err != nil {
				log.Fatal(err)
			}
			fmt.Printf("Year: %d, Min(%s): %.3f, Max(%s): %.3f\n", year, variable, minVal, variable, maxVal)
		}
		if err := rows.Err(); err != nil {
			log.Fatal(err)
		}
	}
}
