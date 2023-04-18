from packages.base_package import BasePackage


class fftw(BasePackage):
    name = "fftw"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Archive
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        self.regex_replace = {
            "post_patch": [
                {
                    0: r"(add_library\s+\(\${fftw3_lib}\s+\${SOURCEFILES}\))",
                    1: r"\1\ntarget_compile_options(${fftw3_lib} PRIVATE -DWITH_OUR_MALLOC)",
                    "in_file": "CMakeLists.txt",
                },
            ],
        }

    @property
    def pkg_depends(self):
        return ("libflac", "libopus")

    @property
    def pkg_mirrors(self):
        return [
            {
                "url": "http://ftp.fftw.org/fftw-3.3.10.tar.gz",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "56c932549852cddcfafdab3820b0200c7742675be92179e59e6215b340e26467",
                    },
                ],
            },
            {
                "url": "https://fossies.org/linux/misc/fftw-3.3.10.tar.gz",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "56c932549852cddcfafdab3820b0200c7742675be92179e59e6215b340e26467",
                    },
                ],
            },
        ]

    @property
    def pkg_config(self):
        return (
            "..",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DBUILD_TESTS=OFF",
            "-DENABLE_THREADS=ON",
            "-DENABLE_FLOAT=OFF",
            "-DENABLE_LONG_DOUBLE=OFF",
            "-DENABLE_QUAD_PRECISION=OFF",
            "-DENABLE_SSE=ON",
            "-DENABLE_SSE2=ON",
            "-DENABLE_AVX=ON",
            "-DENABLE_AVX2=ON",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]
