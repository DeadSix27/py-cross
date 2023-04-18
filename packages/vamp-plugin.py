from packages.base_package import BasePackage

import re
class vampplugin(BasePackage):

    name = "vamp-plugin"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Ignore

        self.patches = [
            {"file": 'vamp/vamp-plugin-sdk-2.7.1.patch', "cmd": "patch -p0"} #They rely on M_PI which is gone since c99 or w/e, give them a self defined one and hope for the best.
        ]

        self.make_command = (
            "make",
            "AR={mingw_prefix_dash}ar",
            "PREFIX={target_prefix}",
            "RANLIB={mingw_prefix_dash}ranlib",
            "LD={mingw_prefix_dash}ld",
            "STRIP={mingw_prefix_dash}strip",
            "CXX={mingw_prefix_dash}g++",
            "CC={mingw_prefix_dash}gcc",
        )

    @property
    def pkg_depends(self):
        return ( "libsndfile", )

    @property
    def pkg_url(self):
        return "https://github.com/c4dm/vamp-plugin-sdk"
    
    def pkg_post_download_commands(self):
        self.compiler.runProcess(['cp', '-fv', 'build/Makefile.mingw64', 'Makefile'])

    def pkg_post_build_commands(self):
        self.compiler.runProcess(["cp", "-fv", "libvamp-sdk.a", "{target_prefix}/lib/"])
        self.compiler.runProcess(["cp", "-fv", "libvamp-hostsdk.a", "{target_prefix}/lib/"])
        self.compiler.runProcess(["cp", "-frv", "vamp-hostsdk/", "{target_prefix}/include/"])
        self.compiler.runProcess(["cp", "-frv", "vamp-sdk/", "{target_prefix}/include/"])
        self.compiler.runProcess(["cp", "-frv", "vamp/", "{target_prefix}/include/"])
        self.compiler.runProcess(["cp", "-fv", "pkgconfig/vamp.pc.in", "{target_prefix}/lib/pkgconfig/vamp.pc"])
        self.compiler.runProcess(["cp", "-fv", "pkgconfig/vamp-hostsdk.pc.in", "{target_prefix}/lib/pkgconfig/vamp-hostsdk.pc"])
        self.compiler.runProcess(["cp", "-fv", "pkgconfig/vamp-sdk.pc.in", "{target_prefix}/lib/pkgconfig/vamp-sdk.pc"])

        for file_name in ['vamp.pc', 'vamp-hostsdk.pc', 'vamp-sdk.pc']:
            file_path = self.compiler.pkgConfigPath.joinpath(file_name)
            with open(file_path, 'r') as f:
                file_content = f.read()
            new_content = re.sub(re.compile(r'%PREFIX%'), str(self.compiler.crossPrefix), file_content)
            with open(file_path, 'w') as f:
                f.write(new_content)

    @property
    def pkg_build(self):
        return ("sdkstatic",)

    @property
    def pkg_info(self):
        return {
            "version": "git (master)",
            "fancy_name": "vamp-plugin"
        }