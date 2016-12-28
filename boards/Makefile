

BOARDS=$(subst .yaml,,$(wildcard *.yaml))

HTMLS=$(addsuffix .html,${BOARDS})


all: ${HTMLS}

%.html: %.yaml
	python3 ../src/boarddef.py -b $< -o $@

.PHONY: clean
clean:
	rm -rfv *.html
