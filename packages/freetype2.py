from packages.base_package import BasePackage

class FREETYPE2(BasePackage):

    name = "freetype2"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        # self.git_tag = "VER-2-13-0" #todo

    @property
    def pkg_depends(self):
        return (
            "libpng",
            'bzip2',
            "zlib-ng",
            "harfbuzz",
            "brotli"
            )
    
    @property
    def pkg_url(self):
        return "https://gitlab.freedesktop.org/freetype/freetype.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            "-DCMAKE_TOOLCHAIN_FILE={cmake_toolchain_file}",
            "-GNinja",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            '-DFT_REQUIRE_ZLIB=ON',
            '-DFT_REQUIRE_PNG=ON',
            '-DFT_REQUIRE_HARFBUZZ=ON',
            '-DFT_REQUIRE_REQUIRE_BROTLI=ON',
            "-DFT_REQUIRE_BZIP2=ON",
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]