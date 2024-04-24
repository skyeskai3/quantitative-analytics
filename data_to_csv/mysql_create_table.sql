# the following has been obfuscated for proprietary reasons

CREATE TABLE IF NOT EXISTS tableX (  
    unique_id bigint NOT NULL AUTO_INCREMENT
    PRIMARY KEY (unique_id));

CREATE TABLE IF NOT EXISTS tableY (
	id bigint NOT NULL AUTO_INCREMENT, 
	o double DEFAULT NULL, 
	c double DEFAULT NULL, 
	l double DEFAULT NULL, 
	h double DEFAULT NULL, 
	ts int unsigned DEFAULT NULL, 
	v int DEFAULT NULL,
    PRIMARY KEY (id));
