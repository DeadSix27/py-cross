from packages.base_package import BasePackage

class dlfcnwin32(BasePackage):

    name = "dlfcn-win32"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja

        self.source_subfolder = "_build"

    @property
    def pkg_url(self):
        return "https://github.com/dlfcn-win32/dlfcn-win32.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options} -DTest=1',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=0',
            '-DBUILD_TESTS=0',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]