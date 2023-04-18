from packages.base_package import BasePackage

class XAVS(BasePackage):

    name = "xavs"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.SVN
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
    
        self.autoconf_command = ["./configure"]

    @property
    def pkg_depends(self):
        return ( )

    @property
    def pkg_url(self):
        return "svn://svn.code.sf.net/p/xavs/code/trunk"
    
    @property
    def pkg_config(self):
        return (
            '{autoconf_prefix_options}',
            '--build=x86_64-pc-linux-gnu',
            '--cross-prefix={mingw_prefix_dash}',
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {
            "version": "git (master)",
            "fancy_name": "xavs"
        }