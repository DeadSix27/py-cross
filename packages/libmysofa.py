from packages.base_package import BasePackage

class LIBMYSOFA(BasePackage):

    name = "libmysofa"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        # self.patches = [
            # {"file": "https://github.com/hoene/libmysofa/pull/199/commits/de6e88aa71d44e407b2331059158ed372931aa22.patch"},
        # ]

    @property
    def pkg_depends(self):
        return ["zlib-ng",]
    
    @property
    def pkg_url(self):
        return "https://github.com/hoene/libmysofa"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_STATIC_LIBS=ON',
            '-DBUILD_TESTS=OFF',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DBUILD_TESTS=OFF',
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]