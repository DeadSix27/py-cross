from packages.base_package import BasePackage


class libressl(BasePackage):
	name = "libressl"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make
		self.regex_replace = {
			"post_install": [
				{
					0: r"Libs.private:  -lws2_32 -lbcrypt\n",
					1: r"Libs.private:  -lws2_32 -lbcrypt -ltls\n",
					"in_file": "{pkg_config_path}/libcrypto.pc",
				},
			]
		}

	@property
	def pkg_depends(self):
		return ()

	@property
	def pkg_url(self) -> str:
		return "https://github.com/libressl-portable/portable.git"

	@property
	def pkg_config(self):
		return (
			"{autoconf_prefix_options}",
			"--build=x86_64-pc-linux-gnu",
			"--disable-hardening",
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ("install",)

	@property
	def pkg_info(self):
		return {"version": "git (master)", "fancy_name": "libressl"}