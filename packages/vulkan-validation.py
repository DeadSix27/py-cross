from packages.base_package import BasePackage

class VULKAN_VALIDATION(BasePackage):

	name = "vulkan-validation"

	def __init__(self, compiler):
		super().__init__(compiler)

		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.CMake
		self.build_system = BasePackage.BuildSystem.Ninja
		self.install_system = BasePackage.BuildSystem.Ninja
		self.source_subfolder = "_build"
		# self.git_tag = "v1.3.261"

	@property
	def pkg_cflags(self):
		return ["-O3"]

	@property
	def pkg_depends(self):
		return ()
	
	@property
	def pkg_url(self):
		return "https://github.com/KhronosGroup/Vulkan-ValidationLayers"
	
	@property
	def pkg_config(self):
		return (
			'..',
			'{cmake_prefix_options}',
			'-DCMAKE_INSTALL_PREFIX={target_prefix}',
			)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ["install"]