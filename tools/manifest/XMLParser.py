from collections import OrderedDict
from typing import Dict, List, Optional, Text, Union
from os.path import dirname, join
from xml.parsers import expat
import xml.etree.ElementTree as etree  # noqa: N813


_catalog = join(dirname(__file__), "catalog")

def _wrap_error(e: expat.error) -> etree.ParseError:
    err = etree.ParseError(e)
    err.code = e.code
    err.position = e.lineno, e.offset
    raise err

_names: Dict[Text, Text] = {}
def _fixname(key: Text) -> Text:
    try:
        name = _names[key]
    except KeyError:
        name = key
        if "}" in name:
            name = "{" + name
        _names[key] = name
    return name


_undefined_entity_code: int = expat.errors.codes[expat.errors.XML_ERROR_UNDEFINED_ENTITY]


class XMLParser:
    """
    An XML parser with support for XHTML DTDs and all Python-supported encodings

    This implements the API defined by
    xml.etree.ElementTree.XMLParser, but supports XHTML DTDs
    (therefore allowing XHTML entities) and supports all encodings
    Python does, rather than just those supported by expat.
    """
    def __init__(self, encoding: Optional[Text] = None) -> None:
        self._parser = expat.ParserCreate(encoding, "}")
        self._target = etree.TreeBuilder()
        # parser settings
        self._parser.buffer_text = True
        self._parser.ordered_attributes = True
        self._parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE)
        # parser callbacks
        self._parser.XmlDeclHandler = self._xml_decl
        self._parser.StartElementHandler = self._start
        self._parser.EndElementHandler = self._end
        self._parser.CharacterDataHandler = self._data
        self._parser.ExternalEntityRefHandler = self._external
        self._parser.SkippedEntityHandler = self._skipped
        # used for our horrible re-encoding hack
        self._fed_data: Optional[List[bytes]] = []
        self._read_encoding: Optional[Text] = None

    def _xml_decl(self, version: Text, encoding: Optional[Text], standalone: int) -> None:
        self._read_encoding = encoding

    def _start(self, tag: Text, attrib_in: List[str]) -> etree.Element:
        assert isinstance(tag, str)
        self._fed_data = None
        tag = _fixname(tag)
        attrib: Dict[Union[bytes, Text], Union[bytes, Text]] = OrderedDict()
        if attrib_in:
            for i in range(0, len(attrib_in), 2):
                attrib[_fixname(attrib_in[i])] = attrib_in[i+1]
        return self._target.start(tag, attrib)

    def _data(self, text: Text) -> None:
        self._target.data(text)

    def _end(self, tag: Text) -> etree.Element:
        return self._target.end(_fixname(tag))

    def _external(self, context: Text, base: Optional[Text], system_id: Optional[Text], public_id: Optional[Text]) -> bool:
        if public_id in {
                "-//W3C//DTD XHTML 1.0 Transitional//EN",
                "-//W3C//DTD XHTML 1.1//EN",
                "-//W3C//DTD XHTML 1.0 Strict//EN",
                "-//W3C//DTD XHTML 1.0 Frameset//EN",
                "-//W3C//DTD XHTML Basic 1.0//EN",
                "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN",
                "-//W3C//DTD XHTML 1.1 plus MathML 2.0 plus SVG 1.1//EN",
                "-//W3C//DTD MathML 2.0//EN",
                "-//WAPFORUM//DTD XHTML Mobile 1.0//EN"
        }:
            parser = self._parser.ExternalEntityParserCreate(context)
            with open(join(_catalog, "xhtml.dtd"), "rb") as fp:
                try:
                    parser.ParseFile(fp)
                except expat.error:
                    return False

        return True

    def _skipped(self, name: Text, is_parameter_entity: bool) -> None:
        err = expat.error("undefined entity %s: line %d, column %d" %
                          (name, self._parser.ErrorLineNumber,
                           self._parser.ErrorColumnNumber))
        err.code = _undefined_entity_code
        err.lineno = self._parser.ErrorLineNumber
        err.offset = self._parser.ErrorColumnNumber
        raise err

    def feed(self, data: bytes) -> None:
        if self._fed_data is not None:
            self._fed_data.append(data)
        try:
            self._parser.Parse(data, False)
        except expat.error as v:
            _wrap_error(v)
        except ValueError as e:
            if e.args[0] == 'multi-byte encodings are not supported':
                assert self._read_encoding is not None
                assert self._fed_data is not None
                xml = b"".join(self._fed_data).decode(self._read_encoding).encode("utf-8")
                new_parser = XMLParser("utf-8")
                self._parser = new_parser._parser
                self._target = new_parser._target
                self._fed_data = None
                self.feed(xml)

    def close(self) -> etree.Element:
        try:
            self._parser.Parse("", True)
        except expat.error as v:
            _wrap_error(v)
        return self._target.close()
