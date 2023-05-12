from packages.base_package import BasePackage

class gnulib(BasePackage):

    name = "gnulib"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Ignore
        self.build_system = BasePackage.BuildSystem.Ignore
        self.install_system = BasePackage.BuildSystem.Ignore

    @property
    def pkg_url(self):
        return "https://git.savannah.gnu.org/git/gnulib.git"

    @property
    def pkg_info(self):
        return {
            "version": "git (master)",
            "fancy_name": "gnulib"
        }