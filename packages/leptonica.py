from tkinter import OFF
from packages.base_package import BasePackage

class leptonica(BasePackage): #todo: remove the bullshit cmake files which r generated completely wrong

	name = "leptonica"

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
					0: r"Libs: -L\${libdir} /Requires: libtiff-4 libpng libopenjp2 libjpeg libwebp\\nRequires\.private: libtiff-4 libpng libopenjp2 libjpeg libwebp\\nLibs: -L\${libdir} /",
					1: "Libs: -L${libdir} -lleptonica-4 -ltiff -lpng -lopenjp2 -ljpeg -lwebp\nRequires.private: libtiff-4 libpng libopenjp2 libjpeg libwebp\n",
					"in_file": "{pkg_config_path}/lept.pc",
				},
				# {
				# 	0: r"Libs: -L\${libdir} -lleptonica-(.*)$",
				# 	1: "Libs: -L${libdir} -lleptonica-\\1 -lgif",
				# 	"in_file": "{pkg_config_path}/lept.pc",
				# },
			]
		}

	def pkg_post_install_commands(self):
		self.compiler.runProcess(["mv", "-v", "{pkg_config_path}/lept_Release.pc", "{pkg_config_path}/lept.pc"])

	@property
	def pkg_depends(self):
		return ["zlib", "openjpeg", "libpng", "libwebp", "libjpeg_turbo", "libtiff", 'dlfcn-win32']
	
	@property
	def pkg_env(self):
		return {
			'CFLAGS': "-DOPJ_STATIC",
		}

	@property
	def pkg_url(self) -> str:
		return 'https://github.com/DanBloomberg/leptonica.git'

	@property
	def pkg_config(self):
		return (
			'..',
			'{cmake_prefix_options}',
			'-DCMAKE_INSTALL_PREFIX={target_prefix}',
			'-DBUILD_SHARED_LIBS=OFF',
			'-DSW_BUILD=0',
			'-DBUILD_PROG=OFF',
			'-DBUILD_SHARED_LIBS=OFF',
			'-DSTATIC=1',
			'-DLIBRARY_TYPE=STATIC',
			)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ["install"]