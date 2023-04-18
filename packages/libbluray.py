from packages.base_package import BasePackage

class LIBBLURAY(BasePackage):

    name = "libbluray"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
    
        self.source_subfolder = "_build"

        self.autoconf_command = ["../configure"]

    @property
    def pkg_depends(self):
        return ( "libxml2", "fontconfig", "freetype2" )
    
    @property
    def pkg_url(self):
        return "https://code.videolan.org/videolan/libbluray.git"

    @property
    def pkg_config(self):
        return (
            '{autoconf_prefix_options}',
            '--build=x86_64-pc-linux-gnu',
            '--disable-examples',
            '--disable-silent-rules',

        )

    # @property
    # def pkg_env(self):
    #     return {
    #         'CFLAGS': "",
    #     }

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
            "fancy_name": "libbluray"
        }