from packages.base_package import BasePackage

class AviSynthPlus(BasePackage):

    name = "avisynth"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        
        self.source_subfolder = "_build"
        self.patches = [
            { 'file': 'avisynthplus/fix-version.patch' },
        ]

    @property
    def pkg_url(self):
        return "https://github.com/AviSynth/AviSynthPlus"

    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DHEADERS_ONLY:bool=on',
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
            "fancy_name": "AviSynth+ (Headers only)"
        }