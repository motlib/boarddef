

BOARDS=$(subst .yaml,,$(wildcard *.yaml))

HTMLS=$(addsuffix .html,${BOARDS})


new: clean all

all: ${HTMLS}

%.html: %.yaml
	python3 ../src/boarddef.py -t ../src/templates -o $@ $<

.PHONY: clean
clean:
	rm -rfv *.html
