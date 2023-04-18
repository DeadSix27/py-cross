
from packages.base_package import BasePackage

class zimg(BasePackage): #todo fix by adding -DKVZ_STATIC_LIB to pkgconfig

    name = "zimg"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

        # self.runAutogenInSubSource = True
    
        # self.source_subfolder = "build/linux"
        # self.autoconf_command = [ "./configure" ]

        # self.patches = [
        #     { 'file': 'kvazaar/0001-mingw-workaround.patch' },
        # ]

    @property
    def pkg_depends(self):
        return ( )

    @property
    def pkg_url(self):
        return "https://github.com/sekrit-twc/zimg.git"
    
    @property
    def pkg_config(self):
        return (
            '{autoconf_prefix_options}',
            '--build=x86_64-pc-linux-gnu',
            "--disable-testapp",
            "--disable-example",
            "--disable-unit-test",
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
            "fancy_name": "zimg"
        }