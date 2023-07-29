from packages.base_package import BasePackage

class LIBASS(BasePackage):

    name = "libass"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
        # self.git_tag = "077328ca6715e2e2826881003946640f56cb763c" #todo
    
        self.source_subfolder = "_build"

        self.autoconf_command = [ "../configure" ]

    @property
    def pkg_depends(self):
        return ( 
            "fontconfig", 
            "harfbuzz", 
            "freetype2", 
            "fribidi" 
            )
    
    @property
    def pkg_url(self):
        return "https://github.com/libass/libass.git"

    @property
    def pkg_config(self):
        return (
            '{autoconf_prefix_options}',
            '--build=x86_64-pc-linux-gnu',
            '--enable-fontconfig',
            '--enable-directwrite',
            '--enable-fribidi',
            '--enable-harfbuzz',
            '--enable-freetype',
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
            "fancy_name": "libass"
        }