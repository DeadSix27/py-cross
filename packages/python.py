import shutil
from packages.base_package import BasePackage

class PYTHON(BasePackage):

    name = "python"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Ignore
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Ignore
    

    @property
    def pkg_url(self):
        return "https://github.com/DeadSix27/python_mingw_libs"

    @property
    def pkg_config(self):
        return ()
    
    @property
    def pkg_build(self):
        return (
            "PREFIX={target_prefix}",
            "PYTHON_VERSION=3.11.4",
            "GENDEF=gendef",
            "DLLTOOL={mingw_prefix_dash}dlltool",
        )

    @property
    def pkg_install(self):
        return ()

    @property
    def pkg_info(self):
        return {
            "version": "git (master)",
            "fancy_name": "python libs"
        }