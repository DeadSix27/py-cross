from packages.base_package import BasePackage

class svt_vp9(BasePackage):

	name = "svt-vp9"

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
					"in_file": "Source/Lib/Codec/EbThreads.h"
				},
			]
		}
	@property
	def pkg_depends(self):
		return []

	@property
	def pkg_url(self) -> str:
		return 'https://github.com/OpenVisualCloud/SVT-VP9.git'

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