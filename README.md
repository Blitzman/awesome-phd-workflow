# Awesome Workflow for a PhD

This is a workflow highly inspired by the Simple Research Journal by Julian Straub during my stay at Oculus Research. I liked the simplicity of his approach and saw its potential to combine it with sophisticated but still simple tools for searching or formatting so that not only taking notes is simple but also sharing and refering back to them.

# Table of Contents
1. [Features](#requirements)
2. [The Philosophy](#the-philosophy)
3. [The Toolchain](#the-toolchain)
4. [The Workflow](#the-workflow)
	1. [Setting up Variables and Metadata](#setting-up-variables-and-metadata)
	2. [Creating the Directory Structure](#creating-the-directory-structure)
	3. [Taking Notes](#taking-notes)
		1. [Daily Notes](#daily-notes)
		2. [Paper Notes](#paper-notes)
		3. [Meeting Notes](#meeting-notes)
		4. [Curated Notes](#curated-notes)
	4. [Searching Notes](#searching-notes)
		1. [Search by Tag](#search-by-tag)
	5. [Converting Notes](#converting-notes)

# Features

* Take daily notes.
* Review papers.
* Summarize meetings.

# The Philosophy

In the end, this philosophy is implemented with the following toolchain:

* Markdown with YAML headers as format.
* VIM for text editing.
* Grip for Markdown previewing.
* Pandoc for document conversion.
* Evince for PDF viewing.
* TeX Live as LaTeX distribution.
* Jekyll for websites.

# The Toolchain

## Markdown
## VIM
## Grip
## Evince
## TeX Live
## Jekyll
## Pandoc

# The Workflow

## Setting up Variables and Metadata

Remember to execute `source ~/bashrc.` or reopen the terminal to apply the changes and be able to use new functions, variables, and aliases.

```bash
export PHD_WORKFLOW_HOME="$HOME/phd"
export PHD_WORKFLOW_AUTHOR="Alberto Garcia-Garcia"

export PHD_WORKFLOW_TAG_SEARCH="$PHD_WORKFLOW_HOME/scripts/search_tags.py"
```

## Creating the Directory Structure

Before starting to use this workflow, you must create the following directory structure in your `$PHD_WORKFLOW_HOME` folder.

```
. `$PHD_WORKFLOW_HOME`
+-- entries
+-- papers
+-- meetings
+-- scripts
|   +-- bcolors.py
|   +-- search_tags.py
+-- README.md
```
## Taking Notes

### Daily Notes

The purpose of a daily note is to capture the thoughts of the day for one or various matters. Each note has a title for itself, which usually corresponds to the particular date, one or various authors, a creation date, and a set of tags that will make it easy to classify and refer back to them.

```yaml
---
title: Daily Note Title is Usually Current Date
author: [First Author, Second Author]
date: YYYY-MM-DD
tags: [Tag1, Tag2, Tag3]
---

Daily note content in Markdown format
```

In order to take a daily note easlily, add an alias to your `~/.bashrc` file -- namely `phd_d` -- which will automatically open a file named after the current date with VIM in the notes folder. That alias will call `open_daily_note()` which will create the entry for the current date if it does not exists or reopen it if it does. The entry will be created with a YAML header containing metadata about the title, author, date, and tags. Daily notes will be created in `$PHD_WORKFLOW_HOME/notes/daily`.

```bash
alias phd_d=open_daily_note

open_daily_note()
{
	local FILE="$PHD_WORKFLOW_HOME/notes/daily/$(date +%F).md"

	if [ ! -f ${FILE} ]; then
		echo "Creating new daily note!"
		echo ${FILE}
		touch ${FILE}
		echo "---" >> ${FILE}
		echo "title: $(date +%F)" >> ${FILE}
		echo "author: [$PHD_WORKFLOW_AUTHOR]" >> ${FILE}
		echo "date: $(date +%F)" >> ${FILE}
		echo "tags: [Entry]" >> ${FILE}
		echo "---" >> ${FILE}
		vim ${FILE}
	else
		vim ${FILE}
	fi
}
```

### Paper Notes

The purpose of a paper note is to summarize the most important aspects of a research work, analyze it, and jotdown insights about it to refer to them later if needed. Each paper note has a title, which corresponds to the paper title itself, one or various authors, a creation date, and a set of tags to ease classification and searches. In addition, the note itself contains BibTeX metadata for the paper so that a proper citation can be generated if needed.

```yaml
---
title: Paper Note Title is Usually Paper Title
author: [First Author, Second Author]
date: YYYY-MM-DD
tags: [Tag1, Tag2, Tag3]
bibtex:
  key: 
  type: 
  author: 
  title: 
  year: 
---

Paper note content in Markdown format
```

To take paper notes, add an alias `phd_p` in your `~/.bashrc` file which will automatically open a new paper note file in VIM with the required header and structure. That alias will call `open_paper_note()` which will create a new Markdown file for the paper given its file name as argument. The convention is to use the author surname in lower case and the year of the publication to name the file. In case of many occurrences, just add a letter increasing according to alphabetic ordering, e.g., `urtasun2015a`. The paper will be created with a YAML header containing metadata about the title, author, date, and tags for the note and BibTeX information for the paper. Paper notes will be created in `$PHD_WORKFLOW_HOME/notes/paper`.

```bash
alias phd_p=open_paper_note

open_paper_note()
{
	local FILE="$PHD_WORKFLOW_HOME/notes/paper/$1.md"

	if [ ! -f ${FILE} ]; then
		echo "Creating new paper note!"
		echo ${FILE}
		touch ${FILE}
		echo "---" >> ${FILE}
		echo "title: " >> ${FILE}
		echo "author: [$PHD_WORKFLOW_AUTHOR]" >> ${FILE}
		echo "date: $(date +%F)" >> ${FILE}
		echo "tags: [Paper]" >> ${FILE}
		echo "bibtex:" >> ${FILE}
		echo "  key: " >> ${FILE}
		echo "  type: " >> ${FILE}
		echo "  author: " >> ${FILE}
		echo "  title: " >> ${FILE}
		echo "  year: " >> ${FILE}
		echo "---" >> ${FILE}
		vim ${FILE}
	else
		vim ${FILE}
	fi
}

```

### Meeting Notes

### Curated Notes

## Searching Notes

One of the must-have features of this workflow, according to its philosophy, is an easy-to-use but sophisticated search engine that allows us to easily filter entries in many different ways.


### Search by Tag

Tag searching is implemented by the `search_tags.py` Python script which can be executed as follows:

```bash
python scripts/search_tags.py path --tags [tag1 tag2 ... tagn]
```

where path is a required positional argument that represents the directory of the search and tags is a list of `n` tags separated by a space. This script will search for the specified tags in the `tags` field in each YAML header from each entry. The search script is case-independent (both file and target tags are converted to lowercase). Here is an example searching daily notes for tags 'Dataset' and 'RGB':

```
python scripts/search_tags.py notes/daily/ --tags Dataset RGB
Searching in notes/daily/ for tags ['dataset', 'rgb']...
notes/daily/2017-10-21.md : ['dataset']
notes/daily/2017-10-22.md : ['dataset', 'rgb']
```

To ease the usage, we can add an alias in our `~/.bashrc` file for each kind of note to avoid typing the path each time:

```bash
alias phd_d_st="python $PHD_WORKFLOW_TAG_SEARCH $PHD_WORKFLOW_HOME/notes/daily/ --tags"
alias phd_p_st="python $PHD_WORKFLOW_TAG_SEARCH $PHD_WORKFLOW_HOME/notes/paper/ --tags"
``` 

In this way, the previous example can be simplified to

```
phd_d_st Dataset RGB
Searching in /home/agarciagarcia/phd/notes/daily/ for tags ['dataset', 'rgb']...
/home/agarciagarcia/phd/notes/daily/2017-10-21.md : ['dataset']
/home/agarciagarcia/phd/notes/daily/2017-10-22.md : ['dataset', 'rgb']
```

## Converting Notes

Sometimes it can be useful to convert any entry into a PDF file for sharing, printing, or just for the sake of reading it in a beautiful format. It can also come in handy to convert it to LaTeX to reuse it in a paper or any other LaTeX document. To do this easily, we can add the following function to the `~/.bashrc` file:

```bash
pandoc_convert()
{
	local FILE="$1"
	echo $FILE
	local OUTPUT_FILE="${FILE%%.*}.$2"
	echo $OUTPUT_FILE
	pandoc -s $FILE -o $OUTPUT_FILE
}
```

Then we will be able to call `pandoc_convert entry.md pdf` which will generate a PDF file with the same file name as the entry you provided or `pandoc_convert entry.md tex` to generate a LaTeX source file. For consistency, it is useful to declare another alias for this function

```bash
alias phd_convert=pandoc_convert
```
