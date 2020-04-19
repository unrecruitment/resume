all: output/pavelsimerda.pdf

# Pavel Šimerda
output/pavelsimerda.pdf: data/pavelsimerda.yaml
	python/resume.py $< $@
show-pavelsimerda: output/pavelsimerda.pdf
	xdg-open $<
