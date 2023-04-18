from packages.base_package import BasePackage


class amf(BasePackage):
    name = "amf"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Ignore
        self.build_system = BasePackage.BuildSystem.Ignore
        self.install_system = BasePackage.BuildSystem.Ignore

    def post_download_commands(self):
        self.compiler.runProcess(["mkdir", "-p", "{target_prefix}/include/AMF"])
        self.compiler.runProcess(["cp", "-av", "amf/public/include/.", "{target_prefix}/include/AMF"])

    @property
    def pkg_url(self):
        return "https://github.com/GPUOpen-LibrariesAndSDKs/AMF"

    @property
    def pkg_config(self):
        return ()

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]
