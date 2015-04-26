from elftools.elf.elffile import ELFFile
from elftools.elf.gnuversions import (
    GNUVerSymSection, GNUVerDefSection,
    GNUVerNeedSection,
    )
from elftools.elf.dynamic import DynamicSection, DynamicSegment
from elftools.elf.sections import SymbolTableSection
from elftools.common.py3compat import (
    ifilter, byte2int, bytes2str, itervalues, str2bytes)
from model.libc_binary import LibcBinary


class ElfSymbolsParser:
    def __init__(self, file):
        self.elffile = ELFFile(file)
        self._versioninfo = None

    def parse_all(self):
        self._init_versioninfo()
        self._init_symbols_table()

        lib_binary = LibcBinary()
        lib_binary.symbols = self.symbols_table

        return lib_binary

    def _init_versioninfo(self):
        """ Search and initialize informations about version related sections
            and the kind of versioning used (GNU or Solaris).
        """
        if self._versioninfo is not None:
            return

        self._versioninfo = {'versym': None, 'verdef': None,
                             'verneed': None, 'type': None}

        for section in self.elffile.iter_sections():
            if isinstance(section, GNUVerSymSection):
                self._versioninfo['versym'] = section
            elif isinstance(section, GNUVerDefSection):
                self._versioninfo['verdef'] = section
            elif isinstance(section, GNUVerNeedSection):
                self._versioninfo['verneed'] = section
            elif isinstance(section, DynamicSection):
                for tag in section.iter_tags():
                    if tag['d_tag'] == 'DT_VERSYM':
                        self._versioninfo['type'] = 'GNU'
                        break

        if not self._versioninfo['type'] and (
                self._versioninfo['verneed'] or self._versioninfo['verdef']):
            self._versioninfo['type'] = 'Solaris'

    def _init_symbols_table(self):
        self.symbols_table = list()

        for section in self.elffile.iter_sections():
            if not isinstance(section, SymbolTableSection):
                continue

            if section['sh_entsize'] == 0:
                continue

            for nsym, symbol in enumerate(section.iter_symbols()):
                version = self._symbol_version(nsym)
                self.symbols_table.append(Symbol(
                    nsym= nsym,
                    name= symbol.name,
                    version_filename= version['filename'],
                    version_index= version['index'],
                    version_hidden= version['hidden'],
                    version_name= version['name'],
                    st_info_bind= symbol['st_info']['bind'],
                    st_info_type= symbol['st_info']['type'],
                    st_other_visibility= symbol['st_other']['visibility'],
                    st_value= symbol['st_value'],
                    st_size= symbol['st_size'],
                    st_shndx= symbol['st_shndx'],
                    st_name= symbol['st_name']
                ))

    def _symbol_version(self, nsym):
        """ Return a dict containing information on the
            or None if no version information is available
        """

        symbol_version = dict.fromkeys(('index', 'name', 'filename', 'hidden'))

        if (not self._versioninfo['versym'] or
                nsym >= self._versioninfo['versym'].num_symbols()):
            return None

        symbol = self._versioninfo['versym'].get_symbol(nsym)
        index = symbol.entry['ndx']
        if not index in ('VER_NDX_LOCAL', 'VER_NDX_GLOBAL'):
            index = int(index)

            if self._versioninfo['type'] == 'GNU':
                # In GNU versioning mode, the highest bit is used to
                # store wether the symbol is hidden or not
                if index & 0x8000:
                    index &= ~0x8000
                    symbol_version['hidden'] = True

            if (self._versioninfo['verdef'] and
                    index <= self._versioninfo['verdef'].num_versions()):
                _, verdaux_iter = \
                        self._versioninfo['verdef'].get_version(index)
                symbol_version['name'] = bytes2str(next(verdaux_iter).name)
            else:
                verneed, vernaux = \
                        self._versioninfo['verneed'].get_version(index)
                symbol_version['name'] = bytes2str(vernaux.name)
                symbol_version['filename'] = bytes2str(verneed.name)

        symbol_version['index'] = index
        return symbol_version

