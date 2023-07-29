from packages.base_package import BasePackage

class wavpack(BasePackage):

    name = "wavpack"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        # self.git_tag = "v1.3.0" #todo

    @property
    def pkg_depends(self):
        return ["iconv", "openssl"]
    
    @property
    def pkg_url(self):
        return "https://github.com/dbry/WavPack"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DWAVPACK_ENABLE_THREADS=ON',
            '-DWAVPACK_ENABLE_DSD=ON',
            '-DWAVPACK_INSTALL_DOCS=OFF',
            '-DWAVPACK_INSTALL_CMAKE_MODULE=OFF',
            '-DWAVPACK_BUILD_PROGRAMS=OFF',
            '-DWAVPACK_BUILD_WINAMP_PLUGIN=OFF',
            '-DWAVPACK_BUILD_COOLEDIT_PLUGIN=OFF',
            '-DBUILD_TESTING=OFF',
            '-DWAVPACK_ENABLE_ASM=OFF',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]