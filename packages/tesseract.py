from packages.base_package import BasePackage


class tesseract(BasePackage):
    name = "tesseract"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        self.regex_replace = { #todo fix \include\tesseract\export.h
            "post_patch": [
                {
                    0: r"    if\(LibArchive_FOUND\)\n",
                    1: r'    set(LibArchive_LIBRARIES "!CMD(pkg-config libarchive --libs-only-l)CMD!")\n'
                    r'    message(STATUS "LibArchive Libs: ${LibArchive_LIBRARIES}")\n'
                    r"    if(LibArchive_FOUND)\n",
                    "in_file": "CMakeLists.txt",
                },
                {
                    0: r"set\(LIB_Ws2_32 Ws2_32\)",
                    1: r"set(LIB_Ws2_32 ws2_32)",
                    "in_file": "CMakeLists.txt",
                },
                {
                    0: r"add_executable\(tesseract src/tesseract.cpp\)",
                    "in_file": "CMakeLists.txt",
                },
                {
                    0: r"install\(TARGETS tesseract DESTINATION bin\)",
                    "in_file": "CMakeLists.txt",
                },
                {
                    0: r"target_link_libraries\(tesseract libtesseract\)",
                    "in_file": "CMakeLists.txt",
                },
                {
                    0: r"if\(HAVE_TIFFIO_H AND WIN32\)",
                    1: r"if(FALSE)",
                    "in_file": "CMakeLists.txt",
                },
            ],
            "post_install": [
                {
                    0: r"Requires\.private:(?:[\s]+)?lept[\n\r]+",
                    1: r"Requires.private: lept libarchive\nRequires: lept libarchive\n",
                    "in_file": "{pkg_config_path}/tesseract.pc",
                },
                {
                    0: r"Libs: -L\${libdir} (-ltesseract[0-9]{2})[ \n\r]+",
                    1: r"Libs: -L${libdir} \1 -lws2_32 -lstdc++\n",
                    "in_file": "{pkg_config_path}/tesseract.pc",
                }
            ],
        }

    @property
    def pkg_depends(self):
        return ['leptonica', 'libxml2', 'zlib', 'libarchive', 'libtiff']

    @property
    def pkg_url(self) -> str:
        return "https://github.com/tesseract-ocr/tesseract.git"

    @property
    def pkg_config(self):
        return (
            "..",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DBUILD_TRAINING_TOOLS=OFF",
            "-DSW_BUILD=OFF",
            "-DBUILD_TRAINING_TOOLS=OFF",
            "-DBUILD_TESTS=OFF",
            "-DSTATIC=ON",
            "-DHAVE_LIBARCHIVE=ON",
            "-DLIBRARY_TYPE=STATIC",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]
