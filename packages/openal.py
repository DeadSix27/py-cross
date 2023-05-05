from packages.base_package import BasePackage

class openal(BasePackage):

    name = "openal"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
    
        self.source_subfolder = "_build"
        self.git_tag = "471592b258d798bb706ce92c1ccd4d5794999490"
        # self.patches = [
        #     { "file": "openal/test.patch"}, 
        # ]
        self.regex_replace = {
            "post_install": [
                {
                    0: r"Libs.private: -static-libgcc -lwinmm -latomic -lm\n",
                    1: r"Libs.private: -static-libgcc -lwinmm -latomic -lm -lstdc++\n",
                    "in_file": "{pkg_config_path}/openal.pc",
                },
                {
                    0: r"Libs: -L\${libdir} -lOpenAL32[ \n\r]+",
                    1: r"Libs: -L${libdir} -lOpenAL32 -lwinmm -latomic -lm -lstdc++\n",
                    "in_file": "{pkg_config_path}/openal.pc",
                }
            ]
        }

    @property
    def pkg_depends(self):
        return ()

    @property
    def pkg_url(self):
        return "https://github.com/kcat/openal-soft"

    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            # '-DCMAKE_TOOLCHAIN_FILE=XCompile.txt',
            # '-DEXTRA_INSTALLS=OFF',
            # '-DHOST={target_host}',
            # '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            # '-DCMAKE_INSTALL_BINDIR={target_prefix}/bin',
            # '-DCMAKE_INSTALL_DATADIR={target_prefix}/share',
            # '-DCMAKE_INSTALL_INCLUDEDIR={target_prefix}/include',
            # '-DCMAKE_INSTALL_LIBDIR={target_prefix}/lib',
            # '-DCMAKE_FIND_ROOT_PATH=',
            '-DLIBTYPE=STATIC',
            '-DALSOFT_STATIC_STDCXX=ON',
            '-DALSOFT_STATIC_LIBGCC=ON',
            '-DALSOFT_STATIC_WINPTHREAD=ON',
            '-DALSOFT_UTILS=OFF',
            '-DALSOFT_EXAMPLES=OFF',
            '-DALSOFT_STATIC_LIBGCC=ON',
            '-DALSOFT_BACKEND_PIPEWIRE=OFF',
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {
            "version": "git (master)",
            "fancy_name": "openal"
        }