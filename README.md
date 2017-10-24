# Awesome Workflow for a PhD

This is a workflow highly inspired by the Simple Research Journal by Julian Straub during my stay at Oculus Research. I liked the simplicity of his approach and saw its potential to combine it with sophisticated but still simple tools for searching or formatting so that not only taking notes is simple but also sharing and refering back to them.

# Table of Contents
1. [Features](#requirements)
2. [The Philosophy](#the-philosophy)
3. [The Toolchain](#the-toolchain)
4. [The Workflow](#the-workflow)
	1. [Setting up Variables and Metadata](#setting-up-variables-and-metadata)
	2. [Creating the Directory Structure](#creating-the-directory-structure)
	3. [Daily Notes](#daily-notes)
		1. [Taking Daily Notes](#taking-daily-notes)
		2. [Searching Through Daily Notes](#searching-through-daily-notes)
		3. [Converting Daily Notes](#converting-daily-notes)
	4. [Paper Notes](#paper-notes)
		1. [Taking Paper Notes](#taking-paper-notes)
		2. [Searching Through Paper Notes](#searching-through-paper-notes)
		3. [Converting Paper Notes](#converting-paper-notes)
	5. [Meeting Notes](#meeting-notes)
		1. [Taking Meeting Notes](#taking-meeting-notes)
		2. [Searching Through Meeting Notes](#searching-through-meeting-notes)
		3. [Converting Meeting Notes](#converting-meeting-notes)

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

## Daily Notes

The purpose of a daily note is to capture the thoughts of the day for one or various matters. Each note has a title for itself, which usually corresponds to the particular date, one or various authors, a creation date, and a set of tags that will make it easy to classify and refer back to them.

```yaml
---
title: Entry Title is Usually Current Date
author: [First Author, Second Author]
date: YYYY-MM-DD
tags: [Tag1, Tag2, Tag3]
---

Entry content...
```

### Taking Daily Notes

Add an alias to your `~/.bashrc` file -- namely `phd_n_o` -- which will automatically open a file named after the current date with VIM in the notes folder. That alias will call `open_daily_note()` which will create the entry for the current date if it does not exists or reopen it if it does. The entry will be created with a YAML header containing metadata about the title, author, date, and tags. Daily notes, also referred as entries, will be created in `$PHD_WORKFLOW_HOME/entries`.

```bash
alias phd_n_o=open_daily_note

open_daily_note()
{
	local FILE="$PHD_WORKFLOW_HOME/entries/$(date +%F).md"

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

### Searching Through Daily Notes

One of the must-have features of this workflow, according to its philosophy, is an easy-to-use but sophisticated search engine that allows us to filter entries by tags. Tag searching is implemented by the `search_tags.py` Python script which can be executed as follows:

```bash
python scripts/search_tags.py path --tags [tag1 tag2 ... tagn]
```

where path is a required positional argument that represents the directory of the search and tags is a list of `n` tags separated by a space. This script will search for the specified tags in the `tags` field in each YAML header from each entry. The search script is case-independent (both file and target tags are converted to lowercase). Here is an example:

```
python scripts/search_tags.py entries/ --tags Dataset RGB
Searching in entries/ for tags ['dataset', 'rgb']...
entries/2017-10-21.md : ['dataset']
entries/2017-10-22.md : ['dataset', 'rgb']
```

To ease the usage you can add an alias `phd_n_st` to your `~/.bashrc` file

```bash
alias phd_n_st="python $PHD_WORKFLOW_TAG_SEARCH $PHD_WORKFLOW_HOME/entries/ --tags"
``` 

so that the previous command can be simplified to

```
phd_n_st Dataset RGB
Searching in /home/agarciagarcia/phd/entries/ for tags ['dataset', 'rgb']...
/home/agarciagarcia/phd/entries/2017-10-21.md : ['dataset']
/home/agarciagarcia/phd/entries/2017-10-22.md : ['dataset', 'rgb']
```

### Converting Daily Notes

Sometimes it can be useful to convert any entry into a PDF file for sharing, printing, or just for the sake of reading it in a beautiful format. It can also come in handy to convert it to LaTeX to reuse it in a paper or any other LaTeX document. To do this easily, add the following function to the `~/.bashrc` file:

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

After reopening the terminal or executing `source ~/.bashrc` you will be able to call `pandoc_convert entry.md pdf` which will generate a PDF file with the same file name as the entry you provided or `pandoc_convert entry.md tex` to generate a LaTeX source file. For consistency, it is useful to declare another alias for this function

```bash
alias phd_c=pandoc_convert
```

## Paper Notes

The purpose of a paper note is to summarize the most important aspects of a research work, analyze it, and jotdown insights about it to refer to them later if needed. Each paper note has a title, which corresponds to the paper title itself, one or various authors, a creation date, and a set of tags to ease classification and searches. In addition, the note itself contains BibTeX metadata for the paper so that a proper citation can be generated if needed.

```yaml
---
title: 
author: [Alberto Garcia-Garcia]
date: 2017-10-23
tags: [Autonomous Driving, 3D]
bibtex:
  key: 
  type: 
  author: 
  title: 
  year: 
---

Paper note content...
```

### Taking Paper Notes

Add an alias `phd_p_o` in your `~/.bashrc` file which will automatically open a new paper note file in VIM with the required header and structure. That alias will call `open_paper_note()` which will create a new Markdown file for the paper given its file name as argument. The convention is to use the author surname in lower case and the year of the publication to name the file. In case of many occurrences, just add a letter increasing according to alphabetic ordering, e.g., `urtasun2015a`. The paper will be created with a YAML header containing metadata about the title, author, date, and tags for the note and BibTeX information for the paper. Paper notes will be created in `$PHD_WORKFLOW_HOME/papers`.

```bash
alias phd_p_o=open_paper_note

open_paper_note()
{
	local FILE="$PHD_WORKFLOW_HOME/papers/$1.md"

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

### Searching Through Paper Notes

In the same fashion as with daily notes, we can search paper notes by their tags using the `search_tags.py` script. We can either use directly the script specifying the `papers/` directory as `path` or we can declare another alias in `~/.bashrc` that will do the work for us

```bash
alias phd_p_st="python $PHD_WORKFLOW_TAG_SEARCH $PHD_WORKFLOW_HOME/papers/ --tags"
```

this alias is executed in the same way as the note searching one

```
phd_p_st 3D
Searching in /home/agarciagarcia/phd/papers/ for tags ['3d']...
/home/agarciagarcia/phd/papers/torralba2016.md : ['3d']
/home/agarciagarcia/phd/papers/urtasun2015.md : ['3d']
```

### Converting Paper Notes

Paper notes can be converted either to PDF or TeX using the same function `pandoc_convert paper.md file_format` or short alias `phd_c paper.md file_format` as we do for daily notes.

### Generating BibTeX Entry from a Paper Note

TODO:

## Meeting Notes

TODO: define the purpose of a meeting note and declare its file structure and format.

### Taking Meeting Notes

### Searching Through Meeting Notes

### Converting Meeting Notes
