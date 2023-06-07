import os
import sys
import subprocess
from base64 import b64encode
import dataclasses
from functools import lru_cache
from io import BytesIO
import os
from pathlib import Path
import subprocess
import sys
from dataclasses import dataclass


""" 
Lightweight font module

by: Donald Guiles
    
"""

@dataclass(slots=True)
class FontDirectory:
    
    MAC = os.path.join("Library", "Fonts")
    WINDOWS = os.path.join("C:\\Windows", "Fonts")
    LINUX  = os.path.join("usr", "share", "fonts")
    LINUX_LOCAL = "/usr/local/share/fonts/"


class Fonts:
    def list(user_specific: bool=False) -> list[str]:
        """ List all the font names

        Returns:
            list[str]: list of font names
        """
        if sys.platform.startswith("w"):
            directory = FontDirectory.WINDOWS
        elif sys.platform.startswith("l"):
            if user_specific:
                directory = "~" + "/.fonts/"
            elif not user_specific:
                directory = FontDirectory.LINUX
        elif sys.platform.startswith("d"):
            if user_specific:
                directory = "~" + FontDirectory.MAC
            elif not user_specific:
                directory = FontDirectory.MAC
        else:
            return []
        return [os.path.splitext(x)[0] for x in os.listdir(directory) if not x.startswith(".")]

    def files(user_specific: bool = False):
        """ Return a List of font files used
        example: ['hi_mom.TFF']

        Args:
            user_specific (bool, optional): for linux and mac, for user specific fonts. Defaults to False.

        Returns:
            _type_: _description_
        """
        if sys.platform.startswith("w"):
            directory = FontDirectory.WINDOWS
        elif sys.platform.startswith("l"):
            if user_specific:
                directory = "~" + "/.fonts/"
            elif not user_specific:
                directory = FontDirectory.LINUX
        elif sys.platform.startswith("d"):
            if user_specific:
                directory = "~" + FontDirectory.MAC
            elif not user_specific:
                directory = FontDirectory.MAC
        else:
            return []
        return [x for x in os.listdir(directory) if not x.startswith(".")]

    
    def paths(user_specific: bool=False) -> list[str]:
        """ list the paths to all the font files

        Returns:
            list[str]: list of paths to font files
        """
        if sys.platform.startswith("w"):
            directory = FontDirectory.WINDOWS
        elif sys.platform.startswith("l"):
            if user_specific:
                directory = "~" + "/.fonts/"
            elif not user_specific:
                directory = FontDirectory.LINUX
        elif sys.platform.startswith("d"):
            if user_specific:
                directory = "~" + FontDirectory.MAC
            elif not user_specific:
                directory = FontDirectory.MAC
            return []
        return [os.path.join(directory, x) for x in os.listdir(directory) if not x.startswith(".")]
       
    def path(user_specific: bool=False) -> str:
        """ Return the path to the fonts directory

        Returns:
            str: path to fonts directory
        """
        if sys.platform.startswith("w"):
            directory = FontDirectory.WINDOWS
        elif sys.platform.startswith("l"):
            if user_specific:
                directory = "~" + "/.fonts/"
            elif not user_specific:
                directory = FontDirectory.LINUX
        elif sys.platform.startswith("d"):
            if user_specific:
                directory = "~" + FontDirectory.MAC
            elif not user_specific:
                directory = FontDirectory.MAC
            return []
        return directory
    
    def linux_system_wide_fonts_dir() -> str:
        return  "/usr/share/fonts/"
    
    def linux_system_wide_software_fonts_dir() -> str:
        return  "/usr/local/share/fonts/"
    
    def linux_user_specific_fonts() -> str:
        return "~/.fonts/"
    
    def install(font_path: str):
        if sys.platform.startswith("w"):
            subprocess.run([f"Install-Font -FilePath {font_path}"])
        elif sys.platform.startswith("l"):
            subprocess.run([f"cp {font_path} ~/.fonts/ && fc-cache -f -v"])
        elif sys.platform.startswith("d"):
            subprocess.run([f"cp {font_path} {FontDirectory.MAC}"])
        else:
            return False
        return True
    


font_scalings = {
    'xx-small': 0.579,
    'x-small':  0.694,
    'small':    0.833,
    'medium':   1.0,
    'large':    1.200,
    'x-large':  1.440,
    'xx-large': 1.728,
    'larger':   1.2,
    'smaller':  0.833,
    None:       1.0,
}
stretch_dict = {
    'ultra-condensed': 100,
    'extra-condensed': 200,
    'condensed':       300,
    'semi-condensed':  400,
    'normal':          500,
    'semi-expanded':   600,
    'semi-extended':   600,
    'expanded':        700,
    'extended':        700,
    'extra-expanded':  800,
    'extra-extended':  800,
    'ultra-expanded':  900,
    'ultra-extended':  900,
}
weight_dict = {
    'ultralight': 100,
    'light':      200,
    'normal':     400,
    'regular':    400,
    'book':       400,
    'medium':     500,
    'roman':      500,
    'semibold':   600,
    'demibold':   600,
    'demi':       600,
    'bold':       700,
    'heavy':      800,
    'extra bold': 800,
    'black':      900,
}
_weight_regexes = [
    # From fontconfig's FcFreeTypeQueryFaceInternal; not the same as
    # weight_dict!
    ("thin", 100),
    ("extralight", 200),
    ("ultralight", 200),
    ("demilight", 350),
    ("semilight", 350),
    ("light", 300),  # Needs to come *after* demi/semilight!
    ("book", 380),
    ("regular", 400),
    ("normal", 400),
    ("medium", 500),
    ("demibold", 600),
    ("demi", 600),
    ("semibold", 600),
    ("extrabold", 800),
    ("superbold", 800),
    ("ultrabold", 800),
    ("bold", 700),  # Needs to come *after* extra/super/ultrabold!
    ("ultrablack", 1000),
    ("superblack", 1000),
    ("extrablack", 1000),
    (r"\bultra", 1000),
    ("black", 900),  # Needs to come *after* ultra/super/extrablack!
    ("heavy", 900),
]
font_family_aliases = {
    'serif',
    'sans-serif',
    'sans serif',
    'cursive',
    'fantasy',
    'monospace',
    'sans',
}


# OS Font paths
try:
    _HOME = Path.home()
except Exception:  # Exceptions thrown by home() are not specified...
    _HOME = Path(os.devnull)  # Just an arbitrary path with no children.
MSFolders = \
    r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
MSFontDirectories = [
    r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts',
    r'SOFTWARE\Microsoft\Windows\CurrentVersion\Fonts']
MSUserFontDirectories = [
    str(_HOME / 'AppData/Local/Microsoft/Windows/Fonts'),
    str(_HOME / 'AppData/Roaming/Microsoft/Windows/Fonts'),
]
X11FontDirectories = [
    # an old standard installation point
    "/usr/X11R6/lib/X11/fonts/TTF/",
    "/usr/X11/lib/X11/fonts",
    # here is the new standard location for fonts
    "/usr/share/fonts/",
    # documented as a good place to install new fonts
    "/usr/local/share/fonts/",
    # common application, not really useful
    "/usr/lib/openoffice/share/fonts/truetype/",
    # user fonts
    str((Path(os.environ.get('XDG_DATA_HOME') or _HOME / ".local/share"))
        / "fonts"),
    str(_HOME / ".fonts"),
]
OSXFontDirectories = [
    "/Library/Fonts/",
    "/Network/Library/Fonts/",
    "/System/Library/Fonts/",
    # fonts installed via MacPorts
    "/opt/local/share/fonts",
    # user fonts
    str(_HOME / "Library/Fonts"),
]


def get_fontext_synonyms(fontext):
    """
    Return a list of file extensions that are synonyms for
    the given file extension *fileext*.
    """
    return {
        'afm': ['afm'],
        'otf': ['otf', 'ttc', 'ttf'],
        'ttc': ['otf', 'ttc', 'ttf'],
        'ttf': ['otf', 'ttc', 'ttf'],
    }[fontext]


def list_fonts(directory, extensions):
    """
    Return a list of all fonts matching any of the extensions, found
    recursively under the directory.
    """
    extensions = ["." + ext for ext in extensions]
    return [os.path.join(dirpath, filename)
            # os.walk ignores access errors, unlike Path.glob.
            for dirpath, _, filenames in os.walk(directory)
            for filename in filenames
            if Path(filename).suffix.lower() in extensions]


def windows_font_directory():
    r"""
    Return the user-specified font directory for Win32.  This is
    looked up from the registry key ::

      \\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders\Fonts

    If the key is not found, ``%WINDIR%\Fonts`` will be returned.
    """
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, MSFolders) as user:
            return winreg.QueryValueEx(user, 'Fonts')[0]
    except OSError:
        return os.path.join(os.environ['WINDIR'], 'Fonts')


def get_windows_installed_fonts():
    """List the font paths known to the Windows registry."""
    import winreg
    items = set()
    # Search and resolve fonts listed in the registry.
    for domain, base_dirs in [
            (winreg.HKEY_LOCAL_MACHINE, [windows_font_directory()]),  # System.
            (winreg.HKEY_CURRENT_USER, MSUserFontDirectories),  # User.
    ]:
        for base_dir in base_dirs:
            for reg_path in MSFontDirectories:
                try:
                    with winreg.OpenKey(domain, reg_path) as local:
                        for j in range(winreg.QueryInfoKey(local)[1]):
                            # value may contain the filename of the font or its
                            # absolute path.
                            key, value, tp = winreg.EnumValue(local, j)
                            if not isinstance(value, str):
                                continue
                            try:
                                # If value contains already an absolute path,
                                # then it is not changed further.
                                path = Path(base_dir, value).resolve()
                            except RuntimeError:
                                # Don't fail with invalid entries.
                                continue
                            items.add(path)
                except (OSError, MemoryError):
                    continue
    return items


@lru_cache()
def get_linux_fontconfig_fonts():
    """Cache and list the font paths known to ``fc-list``."""
    try:
        if b'--format' not in subprocess.check_output(['fc-list', '--help']):
            return []
        out = subprocess.check_output(['fc-list', '--format=%{file}\\n'])
    except (OSError, subprocess.CalledProcessError):
        return []
    return [Path(os.fsdecode(fname)) for fname in out.split(b'\n')]


def find_system_fonts(fontpaths=None, fontext='ttf'):
    """
    Search for fonts in the specified font paths.  If no paths are
    given, will use a standard set of system paths, as well as the
    list of fonts tracked by fontconfig if fontconfig is installed and
    available.  A list of TrueType fonts are returned by default with
    AFM fonts as an option.
    """
    fontfiles = set()
    fontexts = get_fontext_synonyms(fontext)

    if fontpaths is None:
        if sys.platform == 'win32':
            installed_fonts = get_windows_installed_fonts()
            fontpaths = []
        else:
            installed_fonts = _get_fontconfig_fonts()
            if sys.platform == 'darwin':
                fontpaths = [*X11FontDirectories, *OSXFontDirectories]
            else:
                fontpaths = X11FontDirectories
        fontfiles.update(str(path) for path in installed_fonts
                         if path.suffix.lower()[1:] in fontexts)

    elif isinstance(fontpaths, str):
        fontpaths = [fontpaths]

    for path in fontpaths:
        fontfiles.update(map(os.path.abspath, list_fonts(path, fontexts)))

    return [fname for fname in fontfiles if os.path.exists(fname)]


def _fontentry_helper_repr_png(fontent):
    from matplotlib.figure import Figure  # Circular import.
    fig = Figure()
    font_path = Path(fontent.fname) if fontent.fname != '' else None
    fig.text(0, 0, fontent.name, font=font_path)
    with BytesIO() as buf:
        fig.savefig(buf, bbox_inches='tight', transparent=True)
        return buf.getvalue()


def _fontentry_helper_repr_html(fontent):
    png_stream = _fontentry_helper_repr_png(fontent)
    png_b64 = b64encode(png_stream).decode()
    return f"<img src=\"data:image/png;base64, {png_b64}\" />"


FontEntry = dataclasses.make_dataclass(
    'FontEntry', [
        ('fname', str, dataclasses.field(default='')),
        ('name', str, dataclasses.field(default='')),
        ('style', str, dataclasses.field(default='normal')),
        ('variant', str, dataclasses.field(default='normal')),
        ('weight', str, dataclasses.field(default='normal')),
        ('stretch', str, dataclasses.field(default='normal')),
        ('size', str, dataclasses.field(default='medium')),
    ],
    namespace={
        '__doc__': """
    A class for storing Font properties.

    It is used when populating the font lookup dictionary.
    """,
        '_repr_html_': lambda self: _fontentry_helper_repr_html(self),
        '_repr_png_': lambda self: _fontentry_helper_repr_png(self),
    }
)

