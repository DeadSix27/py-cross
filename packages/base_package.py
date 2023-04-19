
from ast import Str, main
from enum import Enum
from pathlib import Path
from typing import AnyStr

try:
    from ..main import CrossCompiler
except ImportError:
    pass


class BasePackage:

    name: str

    cmake_command = ["cmake"]
    make_command = ["make"]
    make_install_command = ["make"]
    autoconf_command: list[str] = ["./configure"]
    cargo_command = ["cargo"]
    meson_command = ["meson", "setup"]
    ninja_command = ["ninja"]
    git_recursive = True
    git_shallow_submodules = True
    git_depth = 1
    git_branch = None
    git_tag = None
    autogen_only_reconf = False
    autogen = True
    runAutogenInSubSource = False
    regex_replace = {}

    patches = ()

    source_subfolder = None

    class PackageType(Enum):
        Ignore = -1
        Dependecy = 0
        Product = 1

    class SourceType(Enum):
        Ignore = -1
        Git = 0
        Archive = 1
        SVN = 2
        Mercurial = 3

    class ConfSystem(Enum):
        Ignore = -1
        CMake = 0
        Meson = 1
        Autoconf = 2
        Cargo = 3

    class BuildSystem(Enum):
        Ignore = -1
        Ninja = 0
        Make = 1
        Cargo = 2

    install_system = BuildSystem.Ignore

    def __init__(self, compiler):
        self.compiler: CrossCompiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.build_system = BasePackage.BuildSystem
        self.conf_system = BasePackage.ConfSystem
        self.install_system = BasePackage.BuildSystem.Ninja
        return "None"
    
    def post_make_commands(self): #todo sanitze
        self.compiler.runProcessDebug = True
        print("Running pkg_post_make_commands")
        self.pkg_post_make_commands()
        self.compiler.runProcessDebug = False

    def pkg_post_make_commands(self):
        pass
    
    def post_build_commands(self): #todo sanitze
        print("Running pkg_post_build_commands")
        self.pkg_post_build_commands()
        self.compiler.runProcessDebug = False

    def pkg_post_build_commands(self):
        pass
        
    
    def post_install_commands(self): #todo sanitze
        self.compiler.runProcessDebug = True
        print("Running pkg_post_install_commands")
        self.pkg_post_install_commands()
        self.compiler.runProcessDebug = False

    def pkg_post_install_commands(self):
        pass
    
    def post_download_sub_commands(self): #todo sanitze
        self.compiler.runProcessDebug = True
        print("Running pkg_post_download_sub_commands")
        self.pkg_post_download_sub_commands()
        self.compiler.runProcessDebug = False

    def pkg_post_download_sub_commands(self):
        pass
    
    def post_download_commands(self): #todo sanitze
        self.compiler.runProcessDebug = True
        print("Running pkg_post_download_commands")
        self.pkg_post_download_commands()
        self.compiler.runProcessDebug = False

    def pkg_post_download_commands(self):
        pass
        
    def post_regex_replace_cmd(self): #todo sanitze
        self.compiler.runProcessDebug = True
        print("Running pkg_post_regex_replace_cmd")
        self.pkg_post_regex_replace_cmd()
        self.compiler.runProcessDebug = False

    def pkg_post_regex_replace_cmd(self):
        pass

    @property
    def depends(self):
        return self.pkg_depends
    
    @property
    def pkg_depends(self):
        return ()
    
    @property
    def has_patches(self):
        return self.patches is not None and len(self.patches) > 0
    
    @property
    def mirrors(self):
        return self.pkg_mirrors

    @property
    def pkg_mirrors(self):
        return ()

    @property
    def path(self):
        return self.compiler.packagesRoot.joinpath(self.compiler.sanitizeFilename(self.name.lower()))

    @property
    def url(self):
        return self.pkg_url
    @property
    def pkg_url(self) -> str:
        return ""
    @property
    def get_source_subfolder_combined(self):
        if self.source_subfolder:
            return self.path.joinpath(self.source_subfolder)
        return Path()
    @property
    def get_source_subfolder(self):
        if self.source_subfolder is not None:
            return Path(self.source_subfolder)
        return Path()
    @property
    def build(self):
        return (() if self.build_system == self.BuildSystem.Cargo else ('-j8',)) + tuple(self.compiler.format_variable_list(self.pkg_build))
        # return self.compiler.format_variable_list(self.pkg_build)
    @property
    def pkg_build(self):
        return ()
    @property
    def pkg_config(self) -> list[str]:
        return []
    @property
    def config(self):
        return self.compiler.format_variable_list(self.pkg_config)
    
    @property
    def pkg_install(self):
        return ()
    @property
    def install(self):
        return self.compiler.format_variable_list(self.pkg_install)
    
    @property
    def pkg_env(self):
        return {}
    
    @property
    def env(self):
        return self.pkg_env