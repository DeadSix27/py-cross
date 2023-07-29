from packages.base_package import BasePackage

class LIBJXL(BasePackage): #todo fix missing -lstdc++

    name = "libjxl"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        # self.git_tag = "5f3cc36bca9e43cf78aa5b819b74b387c638cac5"
        # self.git_tag ="v0.8.1" #todo

        self.regex_replace = {
			"post_install": [
				{
					0: r"Cflags: -I\${includedir}\n",
					1: r"Cflags: -I${includedir}  -DJXL_STATIC_DEFINE\n",
					"in_file": "{pkg_config_path}/libjxl.pc",
				},
				{
					0: r"Cflags: -I\${includedir}\n",
					1: r"Cflags: -I${includedir} -DJXL_THREADS_STATIC_DEFINE\n",
					"in_file": "{pkg_config_path}/libjxl_threads.pc",
				},
				{
					0: r"Libs: -L\${libdir} -ljxl\n",
					1: r"Libs: -L${libdir} -ljxl -lstdc++\n",
					"in_file": "{pkg_config_path}/libjxl.pc",
				},
				{
					0: r"Libs: -L\${libdir} -ljxl_threads\n",
					1: r"Libs: -L${libdir} -ljxl_threads -lstdc++\n",
					"in_file": "{pkg_config_path}/libjxl_threads.pc",
				},
			]
		}

    @property
    def pkg_depends(self):
        return ( "brotli","lcms2","highway", "libjpeg_turbo")
    
    @property
    def pkg_url(self):
        return "https://github.com/libjxl/libjxl"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_TESTING=OFF',
            '-DJPEGXL_ENABLE_DEVTOOLS=OFF',
            '-DJPEGXL_ENABLE_TOOLS=OFF',
            '-DJPEGXL_ENABLE_JPEGLI_LIBJPEG=ON',
            '-DJPEGXL_ENABLE_DOXYGEN=OFF',
            '-DJPEGXL_ENABLE_MANPAGES=OFF',
            '-DJPEGXL_ENABLE_EXAMPLES=OFF',
            '-DJPEGXL_BUNDLE_LIBPNG=OFF',
            '-DJPEGXL_ENABLE_SJPEG=ON',
            '-DJPEGXL_ENABLE_OPENEXR=ON',
            '-DJPEGXL_ENABLE_SKCMS=ON',
            '-DJPEGXL_ENABLE_VIEWERS=OFF',
            '-DJPEGXL_STATIC=ON',
            '-DJPEGXL_FORCE_SYSTEM_BROTLI=ON',
            '-DJPEGXL_FORCE_SYSTEM_LCMS2=ON',
            '-DJPEGXL_FORCE_SYSTEM_HWY=ON',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]