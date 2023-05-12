from packages.base_package import BasePackage

class FRIBIDI(BasePackage):

    name = "fribidi"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Meson
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        self.patches = [
            {"file": "https://github.com/fribidi/fribidi/pull/195.patch" },
        ]

    @property
    def pkg_depends(self):
        return (  )
    
    @property
    def pkg_url(self):
        return "https://github.com/fribidi/fribidi"

    @property
    def pkg_config(self):
        return (
            '..',
            '--prefix={target_prefix}',
            '--cross-file={meson_env_file}',
            '--default-library=static',
            '-Ddocs=false',
            '-Dbin=false',
            '-Dtests=false',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]