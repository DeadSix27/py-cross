from packages.base_package import BasePackage

class svt_av1(BasePackage):

	name = "svt-av1"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.CMake
		self.build_system = BasePackage.BuildSystem.Ninja
		self.install_system = BasePackage.BuildSystem.Ninja
		self.source_subfolder = "_build"
		self.regex_replace = {
			"post_patch": [
				{
					0: r"#include <Windows\.h>",
					1: "#include <windows.h>",
					"in_file": "Source/App/EncApp/EbAppMain.c"
				},
				{
					0: r"#include <Windows\.h>",
					1: "#include <windows.h>",
					"in_file": "Source/Lib/Common/Codec/EbThreads.h"
				},
				{
					0: r"-D_FORTIFY_SOURCE=2",
					1: "-D_FORTIFY_SOURCE=0",
					"in_file": "CMakeLists.txt"
				},
				{
					0: r"-D_FORTIFY_SOURCE=2",
					1: "-D_FORTIFY_SOURCE=0",
					"in_file": "gstreamer-plugin/CMakeLists.txt"
				}
			]
		}

	@property
	def pkg_depends(self):
		return []

	@property
	def pkg_url(self) -> str:
		return 'https://gitlab.com/AOMediaCodec/SVT-AV1'

	@property
	def pkg_config(self):
		return (
			'..',
			'{cmake_prefix_options}',
			'-DCMAKE_INSTALL_PREFIX={target_prefix}',
			'-DBUILD_SHARED_LIBS=OFF',
			'-DCPPAN_BUILD=OFF',
			)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ["install"]