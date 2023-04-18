from packages.base_package import BasePackage

class x265_12(BasePackage):

    name = "x265_12"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Mercurial
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ignore
        self.source_subfolder = "_build"

        #'mv -fv "{offtree_prefix}/libx265_12bit/lib/libx265.a" "{offtree_prefix}/libx265_12bit/lib/libx265_main12.a"'

    @property
    def pkg_depends(self):
        return ( )
    
    @property
    def pkg_url(self):
        return "http://hg.videolan.org/x265/"
    
    @property
    def pkg_config(self):
        return (
            '../source',
            '{cmake_prefix_options}',
            # '-DCMAKE_AR={cross_prefix_full}ar '
            '-DENABLE_ASSEMBLY=ON',
            '-DHIGH_BIT_DEPTH=ON',
            '-DEXPORT_C_API=OFF',
            '-DENABLE_SHARED=OFF',
            '-DENABLE_CLI=OFF',
		    '-DMAIN12=ON',
            '-DCMAKE_INSTALL_PREFIX=.',
            # '-DCMAKE_INSTALL_PREFIX={offtree_prefix}/libx265_10bit'
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]