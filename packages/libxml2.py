from packages.base_package import BasePackage

class LIBXML2(BasePackage): #todo, important: fix pkg config file, cuu needs ++ and dt after, like:  -lz -llzma  -liconv -licudt -licuin -licuuc  -licudt -lstdc++ -lws2_32 

    name = "libxml2"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
    
        self.source_subfolder = "_build"

        self.regex_replace = {
			"post_install": [
				{
					0: r"Libs.private: -lz -llzma  -liconv -licudt -licuin -licuuc  -lws2_32 \n",
					1: r"Libs.private: -lz -llzma  -liconv -licuin -licuuc -licudt -lstdc++ -lws2_32 \n",
					"in_file": "{pkg_config_path}/libxml-2.0.pc",
				},
				{
					0: r"Libs: -L\${libdir} -lxml2",
					1: r"Libs: -L${libdir} -lxml2 -lz -llzma  -liconv -licuin -licuuc -licudt -lstdc++ -lws2_32 \n",
					"in_file": "{pkg_config_path}/libxml-2.0.pc",
				},
			]
		}

    @property
    def pkg_depends(self):
        return ( "bzip2", "zlib-ng", "lzma", "iconv", "icu4c" )

    @property
    def pkg_url(self):
        return "https://gitlab.gnome.org/GNOME/libxml2.git"

    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DLIBXML2_WITH_DEBUG=OFF',
            '-DLIBXML2_WITH_FTP=ON',
            '-DLIBXML2_WITH_HTML=ON',
            '-DLIBXML2_WITH_HTTP=ON',
            '-DLIBXML2_WITH_ICONV=ON',
            '-DLIBXML2_WITH_ICU=ON',
            '-DLIBXML2_WITH_LZMA=ON',
            '-DLIBXML2_WITH_MODULES=ON',
            '-DLIBXML2_WITH_OUTPUT=ON',
            '-DLIBXML2_WITH_PATTERN=ON',
            '-DLIBXML2_WITH_PROGRAMS=OFF',
            '-DLIBXML2_WITH_PUSH=ON',
            '-DLIBXML2_WITH_PYTHON=OFF',
            '-DLIBXML2_WITH_READER=ON',
            '-DLIBXML2_WITH_REGEXPS=ON',
            '-DLIBXML2_WITH_SAX1=ON',
            '-DLIBXML2_WITH_SCHEMAS=ON',
            '-DLIBXML2_WITH_SCHEMATRON=ON',
            '-DLIBXML2_WITH_TESTS=OFF',
            '-DLIBXML2_WITH_THREADS=ON',
            '-DLIBXML2_WITH_TREE=ON',
            '-DLIBXML2_WITH_VALID=ON',
            '-DLIBXML2_WITH_WRITER=ON',
            '-DLIBXML2_WITH_XINCLUDE=ON',
            '-DLIBXML2_WITH_XPATH=ON',
            '-DLIBXML2_WITH_XPTR=ON',
            '-DLIBXML2_WITH_XPTR_LOCS=ON',
            '-DLIBXML2_WITH_ZLIB=ON',
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
            "fancy_name": "libxml2"
        }