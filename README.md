# Web-EPANET

### Requirements

```
    export FLASK_APP=web_epanet.py
    flask run
```

### About

It's a JavaScript application that edits a text file in the browser.

The code takes in a structured text file ".inp" and outputs a modified version of that same file. 

The main part of the code parses the text file, adapts the network it represents, and then spits out a new file. 

The input/output files are EPANET files that are white-space separated with optional semi-colons at the end of each line. 

The sections have keyword headers ([PIPES]), but some of these can be absent. 

The work flow is demonstrated by the files under `app/lib`. The example modifies all junctions. Ideally it would skip junctions (not create a tank) if they start with a user selectable string (e.g. SKIP or S_). In a perfect world, another string (e.g., ROOF) would create a tank at a different height than the default height. 

Examples of .inp input files can be here: https://emps.exeter.ac.uk/engineering/research/cws/resources/benchmarks/design-resiliance-pareto-fronts/data-files/

The code is only physically correct if the .inp file starts with hydraulic units of LPS. Additionally, it assumed Hazel-Williams is used for friction factor, but it's an easy tweak to make it work for Darcy-Weissbach also.

Use WNTR python package to parse the .inp files

### Using the code 

This code can be used by anyone who would like to, with permission of authors. The javascript was adapted from certain python scripts to fit the web. For permission or any inquiries, please contact dtaylor@mit.edu 