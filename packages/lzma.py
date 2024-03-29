from packages.base_package import BasePackage

class LZMA(BasePackage):

    name = "lzma"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja

        self.git_tag = "e3288fdb45c580cb849f6799cf419c4922004ae5"

        self.source_subfolder = "_build"


        self.patches = [
            { 'file': 'lzma/0001-add-pc-file-for-windows.patch' },
            { 'file': 'lzma/0002-temp-llvm-build-fix.patch' },
        ]

        

    @property
    def pkg_url(self):
        return "https://github.com/tukaani-project/xz"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DENABLE_THREADS=ON',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]