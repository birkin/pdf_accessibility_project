# VeraPDF Corpus Summary

- __Source JSON__: `pdf_accessibility_project/VeraPDF_Corpus_Summary.json`
- __Generated__: 2025-09-08, by GPt-5 (low-reasoning) in Windsurf

## Overview
This document summarizes the VeraPDF test corpus, organized by standards and profiles (e.g., ISO 32000, PDF/A, PDF/UA). Each directory contains targeted pass/fail PDFs designed to exercise specific clauses of the corresponding standards.

---

## Directories

### ISO 32000-1
- __Description__: This directory contains a handful of test files for the base PDF 1.7 specification (ISO 32000-1). The naming pattern (e.g., 6-2-2-t01-fail-a) indicates the section and test case number. Each file deliberately breaks or exercises a specific provision of the PDF specification, such as the format of the cross‑reference table, object numbering or signature dictionaries. Because these files are meant for the PDF/A validator, none of them are fully conformant PDF/A documents; instead they expose edge cases for the underlying PDF specification.
- __Files__:
  - `veraPDF test suite 6-2-2-t01-fail-a.pdf`: Exercises Section 6.2.2 of ISO 32000‑1, which covers the document header and version. This file deliberately omits or mis‑formats the header so that a validator can detect the error.
  - `veraPDF test suite 6-2-3-2-t01-fail-b.pdf`: Targets Section 6.2.3.2 dealing with the ID entry in the trailer dictionary. The file is crafted with an invalid or missing ID array so that the validator reports a failure.
  - `veraPDF test suite 6-8-2-2-t01-fail-d.pdf`: Exercises Section 6.8.2.2 concerning digital signatures and signature dictionaries. This document includes a malformed signature dictionary or unsigned references, which should cause a validation failure.
  - `veraPDF test suite 6-8-3-3-t01-fail-a.pdf`: Tests Section 6.8.3.3 related to optional content properties. The file sets up optional content groups incorrectly (e.g., missing the OCProperties entry) so that the validator flags the problem.
  - `veraPDF test suite 6-8-3-3-t01-fail-b.pdf`: Another variant of the Section 6.8.3.3 test; it modifies a different aspect of optional content (for example, using a bad view state) to illustrate how diverse failure scenarios are handled.

### ISO 32000-2
- __Description__: Contains PDF 2.0 (ISO 32000‑2) test cases. Compared with PDF 1.7, PDF 2.0 tightened many definitions. The lone file here targets the cross‑reference stream requirements in Section 6.1.3 of PDF 2.0.
- __Files__:
  - `veraPDF test suite 6-1-3-t04-fail-b.pdf`: Crafted to violate Section 6.1.3 of ISO 32000‑2, which defines the trailer and cross‑reference stream. This test uses an improper xref stream (e.g., missing fields or incorrect offsets) so the validator should fail it.

### PDF_A-1a
- __Description__: PDF/A‑1a represents the most stringent profile of PDF/A 1. It requires that documents be fully tagged and that text be mapped to Unicode so they are accessible. The directory is subdivided into sections corresponding to the ISO 19005‑1 specification: fonts (6.3), metadata (6.7) and logical structure (6.8). Each subdirectory contains a mix of pass and fail files; pass files comply with the requirement, while fail files intentionally omit or misuse the feature under test.
- __Files__:
  - `6.3 Fonts/6.3.8 Unicode character maps/...`: Contains test PDFs exercising Section 6.3.8. Each file checks whether a ToUnicode CMap is correctly attached to embedded fonts. Files labelled “fail” omit the CMap or contain an incorrect mapping, whereas “pass” files embed a proper ToUnicode map.
  - `6.7 Metadata/...`: Tests metadata requirements. Files ensure that XMP metadata is present and correctly formatted. Failing files either lack the RDF metadata packet or include invalid schema definitions.
  - `6.8 Logical structure/...`: Checks logical structure and tagging. PDF/A‑1a requires that document content be tagged with structure elements (Heading, Paragraph, etc.) and that the tags map to Unicode. Failing files either lack tags, use incorrect role maps or omit the structure tree root. Passing files provide a complete tag hierarchy.

### PDF_A-1b
- __Description__: PDF/A‑1b is the basic conformance level. It focuses on reliable visual reproduction but does not require tagged structure. The directory mirrors ISO 19005‑1 sections: file structure, graphics, fonts, transparency, annotations, actions, color spaces, and more. Each subfolder holds test documents that either conform (pass) or intentionally break (fail) the corresponding requirement—for example, missing font embedding, prohibited transparency, or invalid annotation flags.
- __Files__:
  - `6.1 File structure/...`: Tests the file header, trailer, cross‑reference table and filters. Fail files omit headers, mis‑size xref tables or use forbidden filters.
  - `6.2 Graphics/...`: Focuses on graphics state, color spaces and images. Tests include use of prohibited encryption, external colour profiles or transparency (disallowed in PDF/A‑1b).
  - `6.3 Fonts/...`: Verifies that all fonts are embedded and have proper encoding. Fail documents reference external fonts or embed fonts with missing glyph maps.
  - `6.4 Transparency/...`: Ensures that transparency operators are not used in PDF/A‑1b. Any use of soft masks or blend modes triggers a failure.
  - `6.5 Annotations/...`: Checks allowed annotation types and flags. Disallowed popup or multimedia annotations cause a failure.
  - `6.6 Actions/...`: PDF/A prohibits actions that trigger external processes (e.g., launch URLs or run JavaScript). Files here demonstrate allowed and disallowed actions.
  - `6.7 Metadata/...`: Similar to PDF/A‑1a but only requires presence of basic XMP metadata; tag structure is not mandatory.
  - `6.8 Logical structure/...`: While PDF/A‑1b does not require tagging, this folder may contain tests ensuring that if tags are present they adhere to the spec (e.g., correct role maps).

### PDF_A-2a
- __Description__: PDF/A‑2 introduces new features from PDF 1.7, including JPEG 2000 images, transparency and layers. Profile 2a retains the accessibility requirements of 1a (tagging and Unicode mapping) but allows the new features. Directories under PDF_A-2a mirror ISO 19005‑2 sections; files illustrate proper and improper use of layers, optional content, embedded files and ICC profiles.
- __Files__:
  - `6.x sections/...`: Each subfolder corresponds to a clause of ISO 19005‑2. Files labelled ‘fail’ illustrate violations such as missing alternate descriptions for layers, unembedded ICC profiles or misuse of object streams.

### PDF_A-2b
- __Description__: Profile 2b relaxes tagging requirements and focuses on visual fidelity while adopting the new PDF 1.7 features permitted in PDF/A‑2. Subdirectories test embedding of JPEG 2000 images, transparency groups, layers, attachments and use of object streams.
- __Files__:
  - `various sections/...`: Each file either demonstrates correct usage (pass) or contains a deliberate error (fail) such as external ICC profiles, prohibited encryption or unmatched colour profiles.

### PDF_A-2u
- __Description__: PDF/A‑2u (the ‘u’ stands for Unicode) sits between 2a and 2b. It requires that all text be mapped to Unicode but does not mandate tagging. Test files verify the presence of ToUnicode maps on all fonts while still allowing untagged content.
- __Files__:
  - `various sections/...`: Pass files embed proper ToUnicode CMaps; fail files omit them for one or more fonts.

### PDF_A-3b/6.8 Embedded files
- __Description__: PDF/A‑3 extends the standard by allowing arbitrary file attachments. The subdirectory 6.8 Embedded files tests Section 6.8 of ISO 19005‑3. Pass files attach permitted file types and provide AFRelationship metadata; fail files attach forbidden types or omit mandatory relationship keys.
- __Files__:
  - `example fail/pass PDFs`: Documents illustrate proper and improper embedding of auxiliary files, such as including an XML invoice with correct AFRelationship or embedding an executable which is disallowed.

### PDF_A-4
- __Description__: PDF/A‑4 aligns with ISO 19005‑4 (based on PDF 2.0) and simplifies conformance levels to a single level. It allows modern features like rich media and 3D while still prohibiting encryption. The tests here verify compliance with the new requirements, such as updated metadata schemas and restrictions on JavaScript.
- __Files__:
  - `various pass/fail PDFs`: Files demonstrate correct use of PDF 2.0 features within PDF/A‑4 as well as common violations (e.g., missing document status in the metadata or the presence of encryption).

### PDF_A-4e
- __Description__: PDF/A‑4e is tailored for engineering documents and allows the inclusion of PRC or U3D 3D models. Files in this directory test embedding of engineering data, ensuring that 3D content and measurement metadata comply with ISO 19005‑4e.
- __Files__:
  - `various engineering test PDFs`: Failing files include unsupported 3D formats or omit required part metadata; passing files properly embed PRC models and specify units and scale.

### PDF_A-4f
- __Description__: PDF/A‑4f is designed for prepress and publishing workflows and allows the embedding of PDF/A files or other packaging formats. Tests here ensure that only permitted embedded formats are used and that the parent and embedded documents share consistent metadata.
- __Files__:
  - `various publishing test PDFs`: Fail files may embed unapproved file types or mismatched metadata; pass files follow the packaging rules.

### PDF_UA-1
- __Description__: PDF/UA‑1 (ISO 14289‑1) defines requirements for universally accessible PDFs. It mandates a complete tag structure, alternate text for figures and proper reading order. The tests verify that documents meet or violate these accessibility requirements.
- __Files__:
  - `assorted accessibility tests`: Files labelled ‘fail’ omit alt text, use incorrect heading levels or include non‑tagged annotations; pass files demonstrate proper tagging, logical order and alt descriptions.

### PDF_UA-2
- __Description__: PDF/UA‑2 updates the accessibility standard for PDF 2.0. The tests focus on new tagging constructs, enhanced role mapping and updated metadata.
- __Files__:
  - `various UA2 test PDFs`: Fail documents misuse new tagging constructs or omit revised metadata; passing documents implement the updated accessibility model correctly.

### TWG test files
- __Description__: Contains miscellaneous test files contributed by the ISO working group and Technical Working Group (TWG). These files explore edge cases or emerging requirements not yet formalised.
- __Files__:
  - `various TWG test PDFs`: Each file targets a specific edge case, such as unusual character encodings, exotic color spaces or rare annotation types.

### Undefined
- __Description__: This catch‑all directory holds test files that do not yet have a clearly assigned section in the PDF/A or PDF/UA standards. They may be experimental or awaiting specification.
- __Files__:
  - `miscellaneous test PDFs`: Pass and fail files here illustrate unusual behaviours—such as combining interactive forms with file attachments—that the standards working group is still evaluating.

---

## Index
- __actions__
  - `PDF_A-1b/6.6 Actions/...`
- __accessibility__
  - `PDF_A-1a/6.8 Logical structure/...`
  - `PDF_UA-1/...`
  - `PDF_UA-2/...`
- __annotations__
  - `PDF_A-1b/6.5 Annotations/...`
- __embedded files__
  - `PDF_A-3b/6.8 Embedded files/...`
  - `PDF_A-4f/...`
- __engineering__
  - `PDF_A-4e/...`
- __file structure__
  - `PDF_A-1b/6.1 File structure/...`
- __fonts__
  - `PDF_A-1a/6.3 Fonts/6.3.8 Unicode character maps/...`
  - `PDF_A-1b/6.3 Fonts/...`
- __graphics__
  - `PDF_A-1b/6.2 Graphics/...`
- __logical structure__
  - `PDF_A-1a/6.8 Logical structure/...`
  - `PDF_A-1b/6.8 Logical structure/...`
- __metadata__
  - `PDF_A-1a/6.7 Metadata/...`
  - `PDF_A-1b/6.7 Metadata/...`
  - `PDF_A-4/...`
- __miscellaneous__
  - `TWG test files/...`
  - `Undefined/...`
- __publishing__
  - `PDF_A-4f/...`
- __transparency__
  - `PDF_A-1b/6.4 Transparency/...`
  - `PDF_A-2b/...`
- __unicode character maps__
  - `PDF_A-1a/6.3 Fonts/6.3.8 Unicode character maps/...`

---

## Meta
- __info__: produced by ChatGPT5-Thinking
- __date__: 2025-09-03
