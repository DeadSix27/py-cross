from packages.base_package import BasePackage

class LIBMODPLUG(BasePackage):

    name = "libmodplug"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        self.regex_replace = {
            'post_patch': [
                {
                    # Will they ever realise that WIN32 is True on MinGW as well where we need pkg-config files and so on?
                    # Use MSVC or a combination of MINGW/WINDOWS/WIN32
                    0: r'if \(NOT WIN32\)',
                    1: r'if (NOT MSVC)',
                    'in_file': 'CMakeLists.txt'
                },
            ]
        }
    @property
    def pkg_depends(self):
        return ( "zlib", ) #todo: find JBIG and LERC?
    
    @property
    def pkg_url(self):
        return "https://github.com/Konstanty/libmodplug.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=OFF',
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]