all:
	python deploy.py >> /tmp/all
	cd baseline && ./configure && make && (cat ../input/workfile | ./efst | ./bb) >> /tmp/all
	python smt.py >> /tmp/all
	python mst.py >> /tmp/all
	mkdir -p output/data
	printf "alg\ttotalLength\tbottleLength\tbottleLengthSST\tterm\tsteiner\ttimeSec\ttimeHour\n" > output/data/data
	grep -v '%' /tmp/all >> output/data/data
	rm /tmp/all

deploy:
	python deploy.py > output/time

smt:
	cd baseline && ./configure && make && (cat prelude.ps; cat ../input/workfile | ./efst | ./bb) > ../output/workfile-efst.ps
	python smt.py >> output/time
	#cd baseline && ./configure && make && (cat prelude.ps; cat ../input/workfile | ./rfst | ./bb) > ../output/workfile-rfst.ps && (cat prelude.ps; cat ../input/workfile | ./efst | ./bb) > ../output/workfile-efst.ps

mst:
	python mst.py >> output/time

clean:
	rm -rf output/* input/* *.pyc && cd baseline && make clean
