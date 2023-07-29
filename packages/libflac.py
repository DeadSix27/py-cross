from packages.base_package import BasePackage

class LIBFLAC(BasePackage):

    name = "libflac"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja

        # self.git_tag = "1.4.2" #todo
    
        self.source_subfolder = "_build"

        self.patches = [
            {"file": "flac/static-fix.patch"}
        ]

    @property
    def pkg_depends(self):
        return ( "libogg", )

    @property
    def pkg_url(self):
        return "https://github.com/xiph/flac.git"

    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_PROGRAMS=OFF',
            '-DBUILD_EXAMPLES=OFF',
            '-DBUILD_TESTING=OFF',
            '-DBUILD_DOCS=OFF',
            '-DINSTALL_MANPAGES=OFF',
            '-DINSTALL_CMAKE_CONFIG_MODULE=OFF',
            '-DBUILD_SHARED_LIB=OFF',
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
            "fancy_name": "libflac"
        }