from packages.base_package import BasePackage

class DAV1D(BasePackage):

    name = "dav1d"

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
        return "https://code.videolan.org/videolan/dav1d.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '--prefix={target_prefix}',
            '--cross-file={meson_env_file}',
            '--default-library=static',
            '-Denable_tools=false',
            '-Denable_examples=false',
            '-Denable_tests=false',
            '-Denable_docs=false',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]