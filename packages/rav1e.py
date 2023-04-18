from packages.base_package import BasePackage

class RAV1E(BasePackage): #todo: fix stdc++

    name = "rav1e"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Ignore
        self.build_system = BasePackage.BuildSystem.Cargo
        self.install_system = BasePackage.BuildSystem.Ignore
        # self.source_subfolder = "_build"

    @property
    def pkg_depends(self):
        return ()
    

    @property
    def pkg_env(self):
        return {
            "CC": "gcc",
            "CXX": "g++",
            "PKG_CONFIG_LIBDIR": "",
            "PKG_CONFIG_PATH": "",
            "TARGET_CC": "{mingw_prefix_dash}gcc",
            "TARGET_LD": "{mingw_prefix_dash}ld",
            "TARGET_CXX": "{mingw_prefix_dash}g++",
            "CROSS_COMPILE": "1",
        }

    @property
    def pkg_url(self):
        return "https://github.com/xiph/rav1e"

    @property
    def pkg_build(self):
        return (
            'cinstall',
            '-v',
            '--prefix={target_prefix}',
            '--library-type=staticlib',
            '--crt-static',
            '--target={rust_target}',
            '--release',
        )