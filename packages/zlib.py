from packages.base_package import BasePackage

class ZLIB(BasePackage):

    name = "zlib"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.patches = [
            { 'file': 'zlib/0001-mingw-workarounds.patch' },   
        ]
        self.source_subfolder = "_build"

    @property
    def pkg_url(self):
        return "https://github.com/madler/zlib.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DINSTALL_PKGCONFIG_DIR={target_prefix}/lib/pkgconfig',
            '-DBUILD_SHARED_LIBS=OFF',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install", )