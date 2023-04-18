
import os
from packages.base_package import BasePackage

class x265(BasePackage):

	name = "x265"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Mercurial
		self.conf_system = BasePackage.ConfSystem.CMake
		self.build_system = BasePackage.BuildSystem.Ninja
		self.install_system = BasePackage.BuildSystem.Ninja
		self.source_subfolder = "_build"

		# 'run_post_build' : [
		# 	'mv -fv libx265.a libx265_main.a',

		# 	'cp -fv {offtree_prefix}/libx265_10bit/lib/libx265_main10.a libx265_main10.a',
		# 	'cp -fv {offtree_prefix}/libx265_12bit/lib/libx265_main12.a libx265_main12.a',

		# 	"\"{cross_prefix_full}ar\" -M <<EOF\nCREATE libx265.a\nADDLIB libx265_main.a\nADDLIB libx265_main10.a\nADDLIB libx265_main12.a\nSAVE\nEND\nEOF",
		# ],
		# 'run_post_install' : [
		# 	'sed -i.bak \'s|-lmingwex||g\' "{pkg_config_path}/x265.pc"',
		# ],


	def pkg_post_build_commands(self):
		print("running build commands")
		self.compiler.runProcess(['mv','-fv','libx265.a','libx265_main.a'])
		
		lib10Path = self.compiler.getPackagePathByName("x265_10").joinpath("libx265.a")
		lib12Path = self.compiler.getPackagePathByName("x265_12").joinpath("libx265.a")
		
		self.compiler.runProcess(['cp','-fv', str(lib10Path) ,'libx265_main10.a'])
		self.compiler.runProcess(['cp','-fv', str(lib12Path) ,'libx265_main12.a'])

		os.system("x86_64-w64-mingw32-ar -M <<EOF\nCREATE libx265.a\nADDLIB libx265_main.a\nADDLIB libx265_main10.a\nADDLIB libx265_main12.a\nSAVE\nEND\nEOF")
		# "testCmd -M <<EOF\nCREATE libx265.a\nADDLIB libx265_main.a\nADDLIB libx265_main10.a\nADDLIB libx265_main12.a\nSAVE\nEND\nEOF"
		
	
	@property
	def pkg_depends(self):
		return ( "x265_10", "x265_12" )
	
	@property
	def pkg_url(self):
		return "http://hg.videolan.org/x265/"
	
	@property
	def pkg_config(self):
		return (
			'../source',
			'{cmake_prefix_options}',
			# '-DCMAKE_AR={cross_prefix_full}ar',
			'-DENABLE_ASSEMBLY=ON',
			'-DENABLE_SHARED=OFF',
			'-DENABLE_CLI:BOOL=OFF',
			'-DEXTRA_LIB="x265_main10.a;x265_main12.a"',
			# '-DEXTRA_LINK_FLAGS="-L{offtree_prefix}/libx265_10bit/lib;-L{offtree_prefix}/libx265_12bit/lib"'
			'-DLINKED_10BIT=ON',
			'-DLINKED_12BIT=ON',
			'-DCMAKE_INSTALL_PREFIX={target_prefix}',
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ["install"]