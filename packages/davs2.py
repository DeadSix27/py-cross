from packages.base_package import BasePackage

class DAVS2(BasePackage):

    name = "davs2"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

        self.runAutogenInSubSource = True
    
        self.source_subfolder = "build/linux"
        self.autoconf_command = ["./configure"]

    @property
    def pkg_depends(self):
        return ( )

    @property
    def pkg_url(self):
        return "https://github.com/pkuvcl/davs2.git"
    
    @property
    def pkg_config(self):
        return (
            '{autoconf_prefix_options}',
            '--build=x86_64-pc-linux-gnu',
            '--cross-prefix={mingw_prefix_dash}',
            '--disable-cli',
            '--disable-win32thread',
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install-lib-static",)

    @property
    def pkg_info(self):
        return {
            "version": "git (master)",
            "fancy_name": "davs2"
        }