from packages.base_package import BasePackage

class OPENJPEG(BasePackage): #todo, fix the annoying left behind .exe in lib\cmake\openjpeg-2.5\OpenJPEGTargets-release.cmake

    name = "openjpeg"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"

        self.regex_replace = {
            "post_download":
            [
                {
                    0: r"^install\(EXPORT OpenJPEGTargets.+",
                    "in_file": "CMakeLists.txt",
                },
                {
                    0: r"install\(\s+FILES\s+\${OPENJPEG_BINARY_DIR}\/OpenJPEGConfig\.cmake\n\s+DESTINATION\s+\${OPENJPEG_INSTALL_PACKAGE_DIR}\n\)",
                    "in_file": "CMakeLists.txt",
                    "multiline": True,
                },
            ]
        }

    @property
    def pkg_depends(self):
        return ( "zlib-ng", "libpng", "libjpeg_turbo", "libtiff" )
    
    @property
    def pkg_url(self):
        return "https://github.com/uclouvain/openjpeg.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DBUILD_STATIC_LIBS=ON',
            '-DBUILD_PKGCONFIG_FILES=ON',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]