from packages.base_package import BasePackage


class BZIP2(BasePackage):
    name = "bzip2"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja

        self.source_subfolder = "_build"
        self.regex_replace = {
            "post_patch": [
                {
                    0: r"ARCHIVE_OUTPUT_NAME bz2_static\)",
                    1: r"ARCHIVE_OUTPUT_NAME bz2)",
                    "in_file": "CMakeLists.txt",
                },
            ],
        }

    @property
    def pkg_url(self):
        return "https://gitlab.com/bzip2/bzip2/"

    @property
    def pkg_config(self):
        return (
            "..",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DENABLE_STATIC_LIB=ON",
            "-DENABLE_SHARED_LIB=OFF",
            "-DENABLE_LIB_ONLY=ON",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]
