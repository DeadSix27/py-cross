from packages.base_package import BasePackage


class LIBTIFF(BasePackage):
    name = "libtiff"

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
                    0: r"Libs: -L\${libdir} -ltiff\n",
                    1: r"Libs: -L${libdir} -ltiff -ldeflate -lm -lz -ljpeg -llzma -lwebp -lsharpyuv\n",
                    "in_file": "{pkg_config_path}/libtiff-4.pc",
                }
            ]
        }

    # Libs: -L${libdir} -ltiff -ldeflate -lm -lz -ljpeg -llzma -lwebp -lsharpyuv

    @property
    def pkg_depends(self):
        return ("zlib-ng", "libdeflate", "libwebp", "lzma")  # todo: find JBIG and LERC?

    @property
    def pkg_url(self):
        return "https://gitlab.com/libtiff/libtiff"

    @property
    def pkg_config(self):
        return (
            "..",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DBUILD_SHARED_LIBS=OFF",
            "-Dtiff-tools=OFF",
            "-Dtiff-tests=OFF",
            "-Dtiff-contrib=OFF",
            "-Dtiff-docs=OFF",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]
