data:
	./data.sh
	R CMD BATCH data.R
	evince Rplots.pdf &

clean:
	rm -rf *~ *.data *.Rout *.pdf run/* && cd src && make clean && cd .. && clear && ls
