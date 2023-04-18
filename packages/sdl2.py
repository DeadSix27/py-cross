from packages.base_package import BasePackage


class sdl2(BasePackage):
    name = "sdl2"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"

        self.git_branch = "SDL2"

        self.regex_replace = {
            "post_download": [
                {
                    0: r"if\(NOT WINDOWS OR CYGWIN OR MINGW\)",
                    1: r"if(NOT APPLE)",
                    "in_file": "CMakeLists.txt",
                },
                {
                    0: r"if\(NOT \(WINDOWS OR CYGWIN OR MINGW\)\)",
                    1: r"if(NOT APPLE)",
                    "in_file": "CMakeLists.txt",
                },
            ]
        }

    @property
    def pkg_env(self):
        return {"DXSDK_DIR": "{target_prefix}/include"}

    @property
    def pkg_depends(self):
        return ()

    @property
    def pkg_url(self):
        return "https://github.com/libsdl-org/SDL"

    @property
    def pkg_config(self):
        return (
            "..",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DSDL_SHARED=OFF",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]
