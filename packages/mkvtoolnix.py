from packages.base_package import BasePackage


class mkvtoolnix(BasePackage):
	name = "mkvtoolnix"

	def __init__(self, compiler):
		super().__init__(compiler)

		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make

		# self.source_subfolder = "_build"

		# self.autoconf_command = ["../configure"]

	@property
	def  pkg_url(self) -> str:
		return "https://gitlab.com/mbunkus/mkvtoolnix.git"

	@property
	def pkg_depends(self):
		return ()

	@property
	def pkg_config(self):
		return (
			"{autoconf_prefix_options}",
			"--build=x86_64-pc-linux-gnu",
			"--prefix={install_path}/mkvtoolnix",
			# "--with-boost={target_prefix}",
			# "--with-boost-system=boost_system",
			# "--with-boost-filesystem=boost_filesystem",
			# "--with-boost-date-time=boost_date_time",
			# "--with-boost-regex=boost_regex",
			# "--enable-optimization",
			"--enable-qt",
			"--enable-static-qt",
			"--with-moc={toolchain_bin_path_two}/moc",
			"--with-uic={toolchain_bin_path_two}/uic ",
			"--with-rcc={toolchain_bin_path_two}/rcc",
			"--with-qmake={toolchain_bin_path_two}/qmake",
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ("install",)

	@property
	def pkg_info(self):
		return {"version": "git (master)", "fancy_name": "lame"}




# {
# 	'repo_type' : 'git',
# 	'recursive_git' : True,
# 	'build_system' : 'rake',
# 	'configure_options':
# 		# '--host={target_host} --prefix={product_prefix}/mkvtoolnix_git.installed --disable-shared --enable-static'
# 		# ' --with-boost={target_prefix} --with-boost-system=boost_system --with-boost-filesystem=boost_filesystem --with-boost-date-time=boost_date_time --with-boost-regex=boost_regex --enable-optimization --enable-qt --enable-static-qt'
# 		# ' --with-moc={mingw_binpath2}/moc --with-uic={mingw_binpath2}/uic --with-rcc={mingw_binpath2}/rcc --with-qmake={mingw_binpath2}/qmake'
# 		#' QT_LIBS="-lws2_32 -lprcre"'
# 	,
# 	'build_options': '-v',
# 	'depends_on' : [
# 		'cmark', 'libfile', 'libflac', 'boost', 'gettext'
# 	],
# 	'packages': {
# 		'ubuntu' : [ 'xsltproc', 'docbook-utils', 'rake', 'docbook-xsl' ],
# 	},
# 	'run_post_install': (
# 		'{cross_prefix_bare}strip -v {output_prefix}/mkvtoolnix_git.installed/bin/mkvmerge.exe',
# 		# '{cross_prefix_bare}strip -v {product_prefix}/mkvtoolnix_git.installed/bin/mkvtoolnix-gui.exe',
# 		'{cross_prefix_bare}strip -v {output_prefix}/mkvtoolnix_git.installed/bin/mkvextract.exe',
# 		# '{cross_prefix_bare}strip -v {product_prefix}/mkvtoolnix_git.installed/bin/mkvinfo-gui.exe',
# 		'{cross_prefix_bare}strip -v {output_prefix}/mkvtoolnix_git.installed/bin/mkvpropedit.exe',
# 		'{cross_prefix_bare}strip -v {output_prefix}/mkvtoolnix_git.installed/bin/mkvinfo.exe',
# 	),
# 	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'mkvtoolnix' },

# }