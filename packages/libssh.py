from packages.base_package import BasePackage

class libssh(BasePackage):

    name = "libssh"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        # self.git_tag = "v1.3.0" #todo

        self.patches = [
            { "file": "libssh/fix_pkg-config.patch" }
        ]

        self.regex_replace = {
            "post_install": [
                {
                    0: r"Cflags: -I",
                    1: r"Cflags: -DLIBSSH_STATIC -I",
                    "in_file": "{pkg_config_path}/libssh.pc",
                },
                {
                    0: r"Libs: -L",
                    1: r"Requires: zlib libcrypto \nLibs: -lws2_32 -L",
                    "in_file": "{pkg_config_path}/libssh.pc",
                },
            ]
        }

    @property
    def pkg_depends(self):
        return ["zlib", "openssl"]
    
    @property
    def pkg_url(self):
        return "https://github.com/CanonicalLtd/libssh"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DWITH_EXAMPLES=OFF',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]