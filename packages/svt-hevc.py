from packages.base_package import BasePackage

class svt_hevc(BasePackage):

	name = "svt-hevc"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.CMake
		self.build_system = BasePackage.BuildSystem.Ninja
		self.install_system = BasePackage.BuildSystem.Ninja
		self.source_subfolder = "_build"

	@property
	def pkg_depends(self):
		return []

	@property
	def pkg_url(self) -> str:
		return 'https://github.com/OpenVisualCloud/SVT-HEVC.git'

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