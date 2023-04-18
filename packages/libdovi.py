from packages.base_package import BasePackage

class LIBDOVI(BasePackage): #todo: fix stdc++

    name = "libdovi"

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
    def pkg_url(self):
        return "https://github.com/quietvoid/dovi_tool.git"

    @property
    def pkg_build(self):
        return (
            'cinstall',
            '-v',
            '--manifest-path=./dolby_vision/Cargo.toml',
            '--prefix={target_prefix}',
            '--target={rust_target}',
            '--release',
            '--library-type=staticlib',
        )