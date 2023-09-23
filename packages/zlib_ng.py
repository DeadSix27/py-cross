from packages.base_package import BasePackage

class ZLIBNG(BasePackage):

	name = "zlib-ng"

	def __init__(self, compiler):
		super().__init__(compiler)

		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.CMake
		self.build_system = BasePackage.BuildSystem.Ninja
		self.install_system = BasePackage.BuildSystem.Ninja
		self.source_subfolder = "_build"

	@property
	def pkg_url(self):
		return "https://github.com/zlib-ng/zlib-ng.git"
	
	@property
	def pkg_config(self):
		return (
			'..',
			'{cmake_prefix_options}',
			'-DCMAKE_INSTALL_PREFIX={target_prefix}',
			'-DWITH_GTEST=OFF',
			'-DBUILD_SHARED_LIBS=OFF',
			"-DZLIB_COMPAT=ON",
			)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ("install", )