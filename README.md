# pdf-accessibility-project

on this page...
- [goal](#goal)
- [installation](#installation)


## goal

To experiment with using veraPDF, and maybe other tools, to check PDF accessibility.

To be determined:
- how to set up veraPDF
- how to call it from a python script
- how to evaluate the results
    - do we want to eventually have "handlers" to auto-address certain issues?
    - do we want binary pass/fail results, or return a list of issues, or something else?


## installation

Installing veraPDF on my mac...

- from https://verapdf.org/software/ clicked the [veraPDF for Mac link][mac-link]
- clicked through the various steps, installing the optional components.
- by default, it installed to `/Users/me/verapdf`

[mac-link]: https://github.com/verapdf/verapdf-app/releases/download/verapdf-1.10.1/verapdf-1.10.1-mac.dmg



## initial test usage

```bash
~ % 
~ % which verapdf
verapdf not found
~ % 
~ % cd ~/verapdf 
verapdf % 
verapdf % ls
total 48
480B Sep  3 16:27 ./
3.3K Sep  8 08:07 ../
5.2K Sep  3 13:11 .installationinformation
974B Sep  3 13:12 auto-install.xml
 96B Sep  3 13:11 bin/
224B Sep  3 13:55 config/
160B Sep  3 13:11 documents/
 96B Sep  3 13:11 model/
416B Sep  3 13:11 plugins/
 96B Sep  3 13:11 profiles/
128B Sep  3 13:12 Uninstaller/
3.7K Sep  3 13:11 verapdf*
4.3K Sep  3 13:11 verapdf-gui*
verapdf % 
verapdf % ./verapdf --version
veraPDF 1.28.2
Built: Tue Jul 15 16:59:00 EDT 2025
Developed and released by the veraPDF Consortium.
Funded by the PREFORMA project.
Released under the GNU General Public License v3
and the Mozilla Public License v2 or later.

verapdf % 
```


## usage resources

- tutorial: <https://py-pdf.github.io/fpdf2/Tutorial.html#tuto-7-creating-pdfa-documents>
    - Note this interesting section: 

            """
            Conformance Classes
            
            Level A (accessible) encompasses all the requirements of the standard, including mapping the content structure and the correct reading order of the document content. Text content must be extractable, and the structure must reflect the natural reading sequence.

            Level B (Basic) guarantees a clear visual reproducibility of the content. Level B is generally easier to generate than Level A, but it does not ensure 100 percent text extraction or searchability. The hassle-free reuse of the content is not necessarily given.
            """


## other resources

- [veraPDF](https://verapdf.org/)
- [veraPDF GitHub](https://github.com/verapdf)
- [veraPDF Corpus](https://github.com/verapdf/verapdf-corpus) (for tests)
    - note that `PDFA` refers to archival pdfs; `PDFUA` refers to accessibility pdfs.
    - [some indication][some-info] of what's being tested from one of the readme's test-suite references.
        - only lists tests for PDFA, not PDFUA.

- https://github.com/docaxess/verapdf-report-generator-cli

[some-info]: <https://github.com/bfocom/pdfa-testsuite/blob/master/description.txt>
