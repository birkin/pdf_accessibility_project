"""
Untested chatgpt-5-thinking patching script applied to the example HH pdf, producing the "partially-patched" (not yet tested) file.
"""

## adds lang, viewer prefs, xmp metadata, and optional markinfo/Marked=true
from datetime import datetime, timezone
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import (
    BooleanObject,
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
    TextStringObject,
)

## inputs/outputs
src = Path('/mnt/data/HH012060_1146.pdf')
dst = Path('/mnt/data/HH012060_1146_tagged_metadata.pdf')

## configurable values
doc_lang = 'en-US'
display_doc_title = True
set_marked_true = True  # note: this does NOT create real tags; it just flips the flag
doc_title_fallback = 'Untitled Document'


## builds a minimal XMP packet with dc:title and PDF/UA identification
def build_xmp_xml(title: str) -> bytes:
    ## builds minimal xmp
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    xmp = f"""<?xpacket begin='﻿' id='W5M0MpCehiHzreSzNTczkc9d'?>
<x:xmpmeta xmlns:x='adobe:ns:meta/'
  x:xmptk='PyPDF2 minimal XMP'>
  <rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'
           xmlns:dc='http://purl.org/dc/elements/1.1/'
           xmlns:xmp='http://ns.adobe.com/xap/1.0/'
           xmlns:pdf='http://ns.adobe.com/pdf/1.3/'
           xmlns:pdfuaid='http://www.aiim.org/pdfua/ns/id/'>
    <rdf:Description rdf:about=''
        xmp:CreateDate='{now}'
        xmp:ModifyDate='{now}'
        pdfuaid:part='1'
        pdf:Producer='PyPDF2'>
      <dc:title>
        <rdf:Alt>
          <rdf:li xml:lang='x-default'>{title}</rdf:li>
        </rdf:Alt>
      </dc:title>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end='w'?>"""
    return xmp.encode('utf-8')


## read source
reader = PdfReader(str(src))
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

## derive a title for XMP if available
pdf_info = reader.metadata or {}
title = (pdf_info.title if getattr(pdf_info, 'title', None) else None) or doc_title_fallback

## set /Lang on Catalog
root = writer._root_object  # noqa: SLF001 (accessing protected member by design for Catalog entries)
root.update({NameObject('/Lang'): TextStringObject(doc_lang)})

## set /ViewerPreferences/DisplayDocTitle
vp_dict = DictionaryObject()
vp_dict.update({NameObject('/DisplayDocTitle'): BooleanObject(display_doc_title)})
root.update({NameObject('/ViewerPreferences'): vp_dict})

## optionally add /MarkInfo/Marked=true (does NOT create tags)
if set_marked_true:
    markinfo = DictionaryObject()
    markinfo.update({NameObject('/Marked'): BooleanObject(True)})
    root.update({NameObject('/MarkInfo'): markinfo})

## add XMP metadata stream at Catalog level
xmp_stream = DecodedStreamObject()
xmp_stream.set_data(build_xmp_xml(title))
xmp_stream.update(
    {
        NameObject('/Type'): NameObject('/Metadata'),
        NameObject('/Subtype'): NameObject('/XML'),
    }
)
root.update({NameObject('/Metadata'): xmp_stream})

## write out
with open(dst, 'wb') as f:
    writer.write(f)

## basic confirmation to display
{
    'output_pdf': str(dst),
    'size_bytes': dst.stat().st_size,
    'settings': {
        'Lang': doc_lang,
        'DisplayDocTitle': display_doc_title,
        'Marked_true': set_marked_true,
        'Title_used_for_XMP': title,
    },
}
