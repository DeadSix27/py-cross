from packages.base_package import BasePackage

class LENSFUN(BasePackage):

    name = "lensfun"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja

        # self.patches = [
            # { 'file': 'lensfun/0001-fix-mingw-building.patch' },   
        # ]
    
        self.source_subfolder = "_build"

        self.regex_replace = {
			"post_install": [
				{
					0: r"Libs: -L\${libdir} -llensfun\n",
					1: r"Libs: -L${libdir} -llensfun -lstdc++\n",
					"in_file": "{pkg_config_path}/lensfun.pc",
				},
			]
		}


    @property
    def pkg_depends(self):
        return ("glib", )

    @property
    def pkg_url(self):
        return "https://github.com/lensfun/lensfun"

    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_STATIC=ON',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DBUILD_TESTS=OFF',
            '-DBUILD_LENSTOOL=OFF',
            '-DBUILD_DOC=OFF',
            '-DINSTALL_HELPER_SCRIPTS=OFF',
            '-DCMAKE_INSTALL_DATAROOTDIR={target_prefix}/share',
            '-DINSTALL_PYTHON_MODULE=OFF',

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
            "fancy_name": "lensfun"
        }
    
	# 'run_post_patch' : [
	# 	'sed -i.bak \'s/GLIB2_INCLUDE_DIRS/GLIB2_STATIC_INCLUDE_DIRS/\' "../CMakeLists.txt"',
	# 	'sed -i.bak \'s/GLIB2_LIBRARIES/GLIB2_STATIC_LIBRARIES/\' "../CMakeLists.txt"',
	# 	'sed -i.bak \'s/Libs: -L${{libdir}} -llensfun.*/Libs: -L${{libdir}} -llensfun -lstdc++/\' "../libs/lensfun/lensfun.pc.cmake"',
	# ],