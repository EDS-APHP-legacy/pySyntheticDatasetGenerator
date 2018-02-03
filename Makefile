all:
	make clean
	make run
	make ddl
	make load
	make doc
clean:
	rm -rf output/* &&\
	find tmp/ -name "*.csv"  -delete 
load:
	psql -U postgres -h localhost -d postgres -f output/sdgen.sql
doc:
	java -jar lib/schemaSpy_5.0.0.jar -t pgsql -s public -u postgres -db postgres -host localhost -p postgres -hq -dp lib/postgresql-9.4.1212.jre7.jar -o output/doc
ddl:
	liquibase/liquibase.sh liquibase/postgres.properties output/generate_schema.yml > output/sdgen.sql
run:
	python main.py --core=4 --conf=config/example.yaml  --locale fr_FR

reinstall:
	pip uninstall -y sdgen
	pip install .

