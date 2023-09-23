from packages.base_package import BasePackage

class GLAD(BasePackage):

	name = "glad"

	def __init__(self, compiler):
		super().__init__(compiler)

		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Ignore
		self.build_system = BasePackage.BuildSystem.Ignore
		self.install_system = BasePackage.BuildSystem.Ignore

	@property
	def pkg_url(self):
		return "https://github.com/Dav1dde/glad.git"
	
	@property
	def pkg_config(self):
		return []

	@property
	def pkg_build(self):
		return []

	@property
	def pkg_install(self):
		return []