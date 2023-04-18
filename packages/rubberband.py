from packages.base_package import BasePackage

class RUBBERBAND(BasePackage): 

    name = "rubberband"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Meson
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"

        # 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/additional_headers/ladspa.h',

    @property
    def pkg_depends(self):
        return ( 'libsamplerate', 'libsndfile', 'vamp-plugin', 'fftw', )
    
    @property
    def pkg_url(self):
        return "https://github.com/breakfastquay/rubberband.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '--prefix={target_prefix}',
            '--cross-file={meson_env_file}',
            '--default-library=static',
            '--buildtype=release',
            '-Dtests=disabled',
            '-Dcmdline=disabled',
            '-Djni=disabled',
            '-Dvamp=enabled',
            '-Dresampler=libsamplerate',
            '-Dfft=fftw',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]