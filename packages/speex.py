from packages.base_package import BasePackage

class SPEEX(BasePackage):

    name = "speex"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Meson
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"

    @property
    def pkg_depends(self):
        return (  )
    
    @property
    def pkg_url(self):
        return "https://github.com/xiph/speex"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '--prefix={target_prefix}',
            '--cross-file={meson_env_file}',
            '--default-library=static',
            '-Dtest-binaries=disabled',
            '-Dtools=disabled',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]