from packages.base_package import BasePackage


class SHADERC(BasePackage):
    name = "shaderc"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        self.regex_replace = {
            "post_install": [
                {
                    0: r"lshaderc_shared",
                    1: r"lshaderc_combined -lstdc++",
                    "in_file": "{pkg_config_path}/shaderc.pc",
                }
            ],
        }

    @property
    def pkg_depends(self):
        return ("spirv-cross", "glslang", "spirv-tools", "spirv-headers")

    def pkg_post_download_commands(self):
        self.compiler.createSymlink(
            self.compiler.getPackagePathByName("spirv-headers", True),
            self.path.joinpath("third_party/spirv-headers"),
        )
        self.compiler.createSymlink(
            self.compiler.getPackagePathByName("spirv-tools", True),
            self.path.joinpath("third_party/spirv-tools"),
        )
        self.compiler.createSymlink(
            self.compiler.getPackagePathByName("spirv-cross", True),
            self.path.joinpath("third_party/spirv-cross"),
        )
        self.compiler.createSymlink(
            self.compiler.getPackagePathByName("glslang", True),
            self.path.joinpath("third_party/glslang"),
        )

    @property
    def pkg_url(self):
        return "https://github.com/google/shaderc"

    @property
    def pkg_config(self):
        return (
            "..",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DSHADERC_SKIP_TESTS=ON",
            "-DSHADERC_SKIP_EXAMPLES=ON",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]
