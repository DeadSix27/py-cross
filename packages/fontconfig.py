from packages.base_package import BasePackage

class FONTCONFIG(BasePackage):

    name = "fontconfig"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Meson
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"       
        self.patches = [
            { 'file': 'fontconfig/fix-cmake-bullshit.patch' },
        ]

    @property
    def pkg_depends(self):
        return ["freetype2", "expat"]
    
    @property
    def pkg_url(self):
        return "https://gitlab.freedesktop.org/fontconfig/fontconfig.git"

    @property
    def pkg_config(self):
        return (
            '..',
            '--prefix={target_prefix}',
            '--cross-file={meson_env_file}',
            '--default-library=static',
            # '-Dnls=disabled',
            '-Ddoc=disabled',
            '-Ddoc-txt=disabled',
            '-Ddoc-man=disabled',
            '-Ddoc-pdf=disabled',
            '-Ddoc-html=disabled',
            '-Dtests=disabled',
            '-Dtools=disabled',
            '-Dcache-build=disabled',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]