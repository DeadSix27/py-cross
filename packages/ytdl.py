from packages.base_package import BasePackage


class ytdlp(BasePackage):
	name = "yt-dlp"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Ignore
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Ignore

	@property
	def pkg_url(self):
		return "https://github.com/yt-dlp/yt-dlp"

	@property
	def pkg_build(self):
		return ['yt-dlp']

	
	def pkg_post_build_commands(self):
		self.compiler.runProcess(['mkdir', '-pv', '{install_path}/yt-dlp'])
		self.compiler.runProcess(['cp', '-v', 'yt-dlp', '{install_path}/yt-dlp/yt-dlp'])