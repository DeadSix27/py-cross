from packages.base_package import BasePackage

class LIBDEFLATE(BasePackage):

    name = "libdeflate"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        # self.git_tag = "v1.18" #todo

    @property
    def pkg_depends(self):
        return [ "zlib-ng", ] #todo: find JBIG and LERC?
    
    @property
    def pkg_url(self):
        return "https://github.com/ebiggers/libdeflate.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DLIBDEFLATE_BUILD_STATIC_LIB=ON',
            '-DLIBDEFLATE_BUILD_SHARED_LIB=OFF',
            '-DLIBDEFLATE_USE_SHARED_LIB=OFF',
            '-DLIBDEFLATE_BUILD_TESTS=OFF',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]