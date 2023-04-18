from packages.base_package import BasePackage

class nvcodecheaders(BasePackage):

    name = "nv-codec-headers"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Ignore
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
    

    @property
    def pkg_url(self):
        return 'https://github.com/FFmpeg/nv-codec-headers.git'

    @property
    def pkg_config(self):
        return ()
    
    @property
    def pkg_build(self):
        return (
            "PREFIX={target_prefix}",
        )

    @property
    def pkg_install(self):
        return (
            "PREFIX={target_prefix}",
            "install",
        )

    @property
    def pkg_info(self):
        return {
            "version": "git (master)",
            "fancy_name": "nv-codec-headers"
        }