all: output main

output:	
	mkdir outputs

main: backtracking_search.py input.py kakuro.py maintaining_arc_consistency.py output.py testcases

run: all
	count=$$(ls testcases | wc -l); \
	i=0; \
	while [ $$i -lt $$count ]; do \
		python3 input.py $$i; \
		i=$$((i+1)); \
	done

clean: 
	rm -r outputs