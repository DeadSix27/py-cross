#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Very Alpha.

import os, time, shutil
import subprocess
from pathlib import Path
import errno
from typing import Self

class Event:
	"""
	Event class for managing event handlers.
	"""
	def __init__(self):
		self.handlers = set()

	def any(self):
		"""
		Check if there are any event handlers registered.
		"""
		if len(self.handlers) > 0:
			return True
		else:
			return False

	def handle(self, handler):
		"""
		Register an event handler.
		"""
		self.handlers.add(handler)
		return self

	def unhandle(self, handler):
		"""
		Unregister an event handler.
		"""
		try:
			self.handlers.remove(handler)
		except:
			raise ValueError("Handler is not handling this event, so cannot unhandle it.")
		return self

	def fire(self, *args, **kargs):
		"""
		Trigger the event and call all registered handlers.
		"""
		for handler in self.handlers:
			handler(*args, **kargs)

	def getHandlerCount(self):
		"""
		Get the number of registered event handlers.
		"""
		return len(self.handlers)

	__iadd__ = handle
	__isub__ = unhandle
	__call__ = fire
	__len__ = getHandlerCount

class LLVMInstaller:
	"""
	Class for installing LLVM and related tools.
	"""
	def __init__(self):
		self.debug = True
		self.root = Path(os.getcwd())
		self.work_dir = "work"
		self.work_dir_path = Path(self.work_dir).absolute()
		self.llvm_version = "llvmorg-17.0.1"
		
		self.originalPATH = os.environ["PATH"]
		
		self.llvm_source_dir = self.work_dir_path.joinpath("llvm_source")
		self.llvm_install_dir = self.work_dir_path.joinpath("toolchain")
		self.lldb_source_dir =self.work_dir_path.joinpath("lldb")
		self.bin_dir: Path = self.llvm_install_dir.joinpath("bin")
		self.mingw_source_dir = self.work_dir_path.joinpath("mingw_source")

		self.toolchain_script_path = self.root.joinpath("mingw_toolchain_script")

		self.onStatusUpdate = Event()

		self.log("Running Python3 MinGW+LLVM Build Script")

	def log(self, msg, type=None):
		"""
		Log messages and send them to the event handler.
		"""
		if self.onStatusUpdate.any():
			self.onStatusUpdate("[TOOLCHAIN] " + msg)
		else:
			print(msg)

	def build(self):
		"""
		Build LLVM and related components.
		"""
		self.buildLLVM()
		self.buildLLDB()
		self.stripLLVM()
		self.buildWrappers()
		self.cloneMingw()
		self.buildMingwTools()
		self.buildMingw()
		self.buildCompilerRT()
		self.buildLLVMRuntimes()
		self.buildMingwLibs()
		self.buildCompilerRTSanitizer()
		self.buildOpenMP()
		self.symlinkGCCEH()
		self.createUnwindPC()

	def cd(self, dir):
		"""
		Change the current working directory.
		"""
		self.log(F"cd: {dir}")
		os.chdir(dir)
	
	def sn(self, target, link_name, isdir=False):
		"""
		Create a symbolic link.
		"""
		try:
			os.symlink(target, link_name, isdir)
			self.log(F"symlink: {target} -> {link_name}")
		except OSError as e:
			if e.errno == errno.EEXIST:
				os.remove(link_name)
				os.symlink(target, link_name, isdir)
				self.log(F"symlink: {target} -> {link_name}")
			else:
				raise e

	def run(self, cmd):
		"""
		Run a shell command.
		"""
		self.log(F"cmd: {cmd}")
		return_code = subprocess.call(cmd, shell=True)

	def cp(self, src, dst):
		"""
		Copy a file.
		"""
		self.log(F"cp: {src} -> {dst}")
		shutil.copy(src, dst)

	def mkdir(self, path):
		"""
		Create a directory.
		"""
		self.log(F"mkdir: {path}")
		os.makedirs(path, exist_ok=True)

	def buildLLVM(self):
		"""
		Build LLVM.
		"""
		self.mkdir(self.work_dir_path)
		self.cd(self.work_dir_path)
		self.mkdir(self.llvm_source_dir)
		self.run(F"git clone https://github.com/llvm/llvm-project.git --branch {self.llvm_version} --depth 1 {self.llvm_source_dir}")
		self.cd(self.llvm_source_dir)
		self.run(F"git apply {self.toolchain_script_path.joinpath('llvm_stat.patch')}")		
		self.cd("llvm")
		self.mkdir("build")
		self.cd("build")
		

		self.run('cmake -G Ninja .. '
			F'-DCMAKE_INSTALL_PREFIX={self.llvm_install_dir} '
			'-DCMAKE_BUILD_TYPE=Release '
			'-DLLVM_ENABLE_ASSERTIONS=OFF '
			'-DLLVM_ENABLE_PROJECTS="clang;lld;lldb;clang-tools-extra" '
			'-DLLVM_TARGETS_TO_BUILD=X86 '
			'-DLLVM_INSTALL_TOOLCHAIN_ONLY=ON '
			'-DLLVM_LINK_LLVM_DYLIB=ON '
			'-DLLVM_TOOLCHAIN_TOOLS="llvm-ar;llvm-ranlib;llvm-objdump;llvm-rc;llvm-cvtres;llvm-nm;llvm-strings;llvm-readobj;llvm-dlltool;llvm-pdbutil;llvm-objcopy;llvm-strip;llvm-cov;llvm-profdata;llvm-addr2line;llvm-symbolizer;llvm-windres;llvm-ml;llvm-readelf;llvm-size" '
		)

		
		# self.run(F"cmake -G Ninja .. -DCMAKE_INSTALL_PREFIX={self.llvm_install_dir} "
		#	 "-DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_ASSERTIONS=OFF "
		#	 '-DLLVM_ENABLE_PROJECTS="clang;lld;lldb;clang-tools-extra" '
		#	 "-DLLVM_TARGETS_TO_BUILD=X86 -DLLVM_INSTALL_TOOLCHAIN_ONLY=ON "
		#	 "-DLLVM_LINK_LLVM_DYLIB=ON "
		#	 '-DLLVM_TOOLCHAIN_TOOLS="llvm-ar;llvm-ranlib;llvm-objdump;llvm-rc;llvm-cvtres;llvm-nm;llvm-strings;llvm-readobj;llvm-dlltool;llvm-pdbutil;llvm-objcopy;llvm-strip;llvm-cov;llvm-profdata;llvm-addr2line;llvm-symbolizer;llvm-windres;llvm-ml;llvm-readelf;llvm-size"'
		# )

		self.run("ninja -j 8")
		self.run("ninja -j 8 install/strip")
		self.cd(self.work_dir_path)

	def buildLLDB(self):
		"""
		Build LLDB.
		"""
		self.run(F"git clone https://github.com/lldb-tools/lldb-mi.git {self.lldb_source_dir}")
		self.cd(self.lldb_source_dir)
		self.mkdir("build")
		self.cd("build")
		os.environ["LLVM_DIR"] = str(self.llvm_source_dir.joinpath("llvm").joinpath("build"))
		self.run(F"cmake -G Ninja -DCMAKE_INSTALL_PREFIX={self.llvm_install_dir} -DCMAKE_BUILD_TYPE=Release ..")
		self.run("ninja -j 8")
		self.run("ninja -j 8 install/strip")
		del os.environ["LLVM_DIR"]
		self.cd(self.work_dir_path)
	
	def stripLLVM(self):
		self.cd(self.llvm_install_dir)
		self.cd('bin')
		self.run('rm -v amdgpu-arch')
		self.run('rm -vf clang-apply-replacements')
		self.run('rm -vf clang-change-namespace')
		self.run('rm -vf clang-check')
		self.run('rm -vf clang-cl')
		self.run('rm -vf clang-doc')
		self.run('rm -vf clang-extdef-mapping')
		self.run('rm -vf clang-include-cleaner')
		self.run('rm -vf clang-include-fixer')
		self.run('rm -vf clang-linker-wrapper')
		self.run('rm -vf clang-move')
		self.run('rm -vf clang-offload-bundler')
		self.run('rm -vf clang-offload-packager')
		self.run('rm -vf clang-pseudo')
		self.run('rm -vf clang-query')
		self.run('rm -vf clang-refactor')
		self.run('rm -vf clang-rename')
		self.run('rm -vf clang-reorder-fields')
		self.run('rm -vf clang-repl')
		self.run('rm -vf clang-scan-deps')
		self.run('rm -v diagtool')
		self.run('rm -v find-all-symbols')
		self.run('rm -v hmaptool')
		self.run('rm -v ld64.lld')
		self.run('rm -v modularize')
		self.run('rm -v nvptx-arch')
		self.run('rm -v pp-trace')
		self.run('rm -v scan-build')
		self.run('rm -v scan-view')
		self.run('rm -v wasm-ld')
		self.cd('..')
		self.run('rm -vrf libexec')
		self.cd('share')
		self.cd('clang')
		self.cd('..')
		self.run('rm -vrf opt-viewer scan-build scan-view')
		self.run('rm -vrf man/man1/scan-build.1')
		self.cd('..')
		self.cd('include')
		self.run('rm -vrf clang clang-c clang-tidy lld llvm llvm-c lldb')
		self.cd('..')
		self.cd('lib')
		self.run('rm -vf *.dll.a')
		self.run('rm -vf lib*.a')
		self.run('rm -rvf libclang.so')
		self.run('rm -rvf libclang.so.17')
		self.run('rm -rvf libclang.so.17.0.1')
		self.run('rm -rvf libLTO.so')
		self.run('rm -rvf libLTO.so.17')
		self.run('rm -rvf libRemarks.so')
		self.run('rm -rvf libRemarks.so.17')
		self.run('rm -rvf *.dylib*')
		self.run('rm -rvf cmake')
		self.cd('..')

	def buildWrappers(self):
		"""
		Build wrappers for clang and other tools.
		"""
		self.mkdir(self.bin_dir)
		self.cp(self.toolchain_script_path.joinpath("wrappers/objdump-wrapper.sh"), F"{self.bin_dir.joinpath('objdump-wrapper.sh')}")
		self.cp(self.toolchain_script_path.joinpath("wrappers/ld-wrapper.sh"), F"{self.bin_dir.joinpath('ld-wrapper.sh')}")
		self.cp(self.toolchain_script_path.joinpath("wrappers/clang-target-wrapper.sh"), F"{self.bin_dir.joinpath('clang-target-wrapper.sh')}")
		self.run(F"cc {self.toolchain_script_path.joinpath('wrappers/clang-target-wrapper.c')} -o {self.bin_dir.joinpath('clang-target-wrapper')} -O2 -Wl,-s")
		self.run(F"cc {self.toolchain_script_path.joinpath('wrappers/llvm-wrapper.c')} -o {self.bin_dir.joinpath('llvm-wrapper')} -O2 -Wl,-s")
		self.sn(self.bin_dir.joinpath("clang-target-wrapper.sh"), self.bin_dir.joinpath("x86_64-w64-mingw32-clang"))
		self.sn(self.bin_dir.joinpath("clang-target-wrapper.sh"), self.bin_dir.joinpath("x86_64-w64-mingw32-clang++"))
		self.sn(self.bin_dir.joinpath("clang-target-wrapper.sh"), self.bin_dir.joinpath("x86_64-w64-mingw32-gcc"))
		self.sn(self.bin_dir.joinpath("clang-target-wrapper.sh"), self.bin_dir.joinpath("x86_64-w64-mingw32-g++"))
		self.sn(self.bin_dir.joinpath("clang-target-wrapper.sh"), self.bin_dir.joinpath("x86_64-w64-mingw32-c++"))
		self.sn(self.bin_dir.joinpath("clang-target-wrapper.sh"), self.bin_dir.joinpath("x86_64-w64-mingw32-as"))
		self.sn(self.bin_dir.joinpath("llvm-addr2line"), self.bin_dir.joinpath("x86_64-w64-mingw32-addr2line"))
		self.sn(self.bin_dir.joinpath("llvm-ar"), self.bin_dir.joinpath("x86_64-w64-mingw32-ar"))
		self.sn(self.bin_dir.joinpath("llvm-ranlib"), self.bin_dir.joinpath("x86_64-w64-mingw32-ranlib"))
		self.sn(self.bin_dir.joinpath("llvm-nm"), self.bin_dir.joinpath("x86_64-w64-mingw32-nm"))
		self.sn(self.bin_dir.joinpath("llvm-objcopy"), self.bin_dir.joinpath("x86_64-w64-mingw32-objcopy"))
		self.sn(self.bin_dir.joinpath("llvm-readelf"), self.bin_dir.joinpath("x86_64-w64-mingw32-readelf"))
		self.sn(self.bin_dir.joinpath("llvm-size"), self.bin_dir.joinpath("x86_64-w64-mingw32-size"))
		self.sn(self.bin_dir.joinpath("llvm-strings"), self.bin_dir.joinpath("x86_64-w64-mingw32-strings"))
		self.sn(self.bin_dir.joinpath("llvm-strip"), self.bin_dir.joinpath("x86_64-w64-mingw32-strip"))
		self.sn(self.bin_dir.joinpath("llvm-ar"), self.bin_dir.joinpath("x86_64-w64-mingw32-llvm-ar"))
		self.sn(self.bin_dir.joinpath("llvm-ranlib"), self.bin_dir.joinpath("x86_64-w64-mingw32-llvm-ranlib"))
		self.sn(self.bin_dir.joinpath("llvm-windres"), self.bin_dir.joinpath("x86_64-w64-mingw32-windres"))
		self.sn(self.bin_dir.joinpath("llvm-dlltool"), self.bin_dir.joinpath("x86_64-w64-mingw32-dlltool"))
		self.sn(self.bin_dir.joinpath("ld-wrapper.sh"), self.bin_dir.joinpath("x86_64-w64-mingw32-ld"))
		self.sn(self.bin_dir.joinpath("objdump-wrapper.sh"), self.bin_dir.joinpath("x86_64-w64-mingw32-objdump"))

		self.mkdir(self.llvm_install_dir.joinpath('x86_64-w64-mingw32'))
		self.cd(self.llvm_install_dir.joinpath('x86_64-w64-mingw32'))
		self.sn("../bin", 'bin', True)
		self.mkdir(self.llvm_install_dir.joinpath('x86_64-w64-mingw32/x86_64-w64-mingw32'))
		self.cd(self.llvm_install_dir.joinpath('x86_64-w64-mingw32/x86_64-w64-mingw32'))
		self.sn("../bin", 'bin', True)
		self.sn("../lib", 'lib', True)
		self.sn("../include", 'include', True)

	def cloneMingw(self):
		"""
		Clone MinGW.
		"""
		self.cd(self.work_dir_path)
		self.run(F"git clone https://github.com/mingw-w64/mingw-w64 {self.mingw_source_dir}")
	
	def buildMingwTools(self):
		"""
		Build MinGW tools.
		"""
		self.cd(self.mingw_source_dir)
		self.cd("mingw-w64-tools/gendef")
		self.mkdir("build")
		self.cd("build")
		self.run(F"../configure --prefix={self.llvm_install_dir}")
		self.run("make -j8")
		self.run("make install-strip")

		self.cd(self.mingw_source_dir)
		self.cd("mingw-w64-tools/widl")
		self.mkdir("build")
		self.cd("build")
		self.run(F"../configure --prefix={self.llvm_install_dir} --target=x86_64-w64-mingw32 --with-widl-includedir={self.llvm_install_dir.joinpath('x86_64-w64-mingw32')}/x86_64-w64-mingw32/include")
		self.run("make -j8")
		self.run("make install-strip")

	def buildMingw(self):
		"""
		Build MinGW.
		"""
		os.environ["PATH"] = F'{self.bin_dir}:{os.environ["PATH"]}'
		self.cd(self.mingw_source_dir)
		# self.run(F"patch -p1 < {self.toolchain_script_path.joinpath('clang_mingw_temp_cpuid.patch')}") 
		self.cd("mingw-w64-headers")
		self.mkdir("build")
		self.cd("build")
		os.environ["INSTALL"] = "install -C"
		self.run(F"../configure --prefix={self.llvm_install_dir.joinpath('x86_64-w64-mingw32')} --enable-idl  --with-default-win32-winnt=0x0A00 --with-default-msvcrt=ucrt")
		self.run("make install")
		self.cd(self.mingw_source_dir)
		self.cd("mingw-w64-crt")
		self.mkdir("build")
		self.cd("build")
		self.run(F"../configure --host=x86_64-w64-mingw32 --prefix={self.llvm_install_dir.joinpath('x86_64-w64-mingw32')} --disable-lib32 --enable-lib64 --with-default-msvcrt=ucrt --enable-cfguard")
		self.run("make install")
		
		self.run(F"llvm-ar rcs {self.llvm_install_dir.joinpath('x86_64-w64-mingw32/lib/libssp.a')}")
		self.run(F"llvm-ar rcs {self.llvm_install_dir.joinpath('x86_64-w64-mingw32/lib/libssp_nonshared.a')}")

		del os.environ["INSTALL"]
		os.environ["PATH"] = self.originalPATH


	def buildCompilerRT(self):
		"""
		Build Compiler-RT.
		"""
		os.environ["PATH"] = F'{self.bin_dir}:{os.environ["PATH"]}'
		# os.environ["LLVM_DIR"] = str(self.llvm_source_dir.joinpath("llvm").joinpath("build"))
		self.cd(self.llvm_source_dir.joinpath("compiler-rt"))
		self.mkdir("buildrt")
		self.cd("buildrt")
		
		self.run("cmake -GNinja ../lib/builtins "
		"-DCMAKE_BUILD_TYPE=Release "
		F"-DCMAKE_INSTALL_PREFIX={self.llvm_install_dir.joinpath('lib/clang/17')} "
		"-DCMAKE_C_COMPILER=x86_64-w64-mingw32-clang "
		"-DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-clang++ "
		"-DCMAKE_SYSTEM_NAME=Windows "
		F"-DCMAKE_AR={self.llvm_install_dir.joinpath('bin/llvm-ar')} "
		F"-DCMAKE_RANLIB={self.llvm_install_dir.joinpath('bin/llvm-ranlib')} "
		"-DCMAKE_C_COMPILER_WORKS=1 "
		"-DCMAKE_CXX_COMPILER_WORKS=1 "
		"-DCMAKE_C_COMPILER_TARGET=x86_64-w64-windows-gnu "
		"-DCOMPILER_RT_DEFAULT_TARGET_ONLY=TRUE "
		"-DCOMPILER_RT_USE_BUILTINS_LIBRARY=TRUE "
		"-DCOMPILER_RT_BUILD_BUILTINS=TRUE "
		"-DLLVM_CONFIG_PATH= "
		F"-DCMAKE_FIND_ROOT_PATH={self.llvm_install_dir.joinpath('x86_64-w64-mingw32')} "
		"-DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY "
		"-DCMAKE_FIND_ROOT_PATH_MODE_PACKAGE=ONLY "
		"-DSANITIZER_CXX_ABI=libc++ "
		"-DCMAKE_C_FLAGS_INIT=-mguard=cf "
		"-DCMAKE_CXX_FLAGS_INIT=-mguard=cf "
		)


		# self.run(
		# 	'cmake '
		# 	'-G"Ninja" '
		# 	'-DCMAKE_BUILD_TYPE=Release '
		# 	F'-DCMAKE_INSTALL_PREFIX="{self.llvm_install_dir.joinpath("lib/clang/17")}" '
		# 	'-DCMAKE_C_COMPILER=x86_64-w64-mingw32-clang '
		# 	'-DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-clang++ '
		# 	'-DCMAKE_SYSTEM_NAME=Windows '
		# 	F'-DLLVM_DIR="{self.llvm_install_dir}" '
		# 	F'-DLLVM_CMAKE_DIR={str(self.llvm_source_dir.joinpath("llvm/cmake/modules"))} '
		# 	F'-DCMAKE_AR="{self.llvm_install_dir.joinpath("bin/llvm-ar")}" '
		# 	F'-DCMAKE_RANLIB="{self.llvm_install_dir.joinpath("bin/llvm-ranlib")}" '
		# 	'-DCMAKE_C_COMPILER_WORKS=1 '
		# 	'-DCMAKE_C_COMPILER_TARGET=x86_64-w64-windows-gnu '
		# 	'-DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY '
		# 	'-DCMAKE_FIND_ROOT_PATH_MODE_PACKAGE=ONLY '
		# 	'../lib/builtins'
		# )
		self.run("ninja")
		self.run("ninja install")
		os.environ["PATH"] = self.originalPATH

	def buildCompilerRTSanitizer(self):
		"""
		Build Compiler-RT Sanitizer.
		"""
		os.environ["PATH"] = F'{self.bin_dir}:{os.environ["PATH"]}'
		# os.environ["LLVM_DIR"] = str(self.llvm_source_dir.joinpath("llvm").joinpath("build"))
		self.cd(self.llvm_source_dir.joinpath("compiler-rt"))
		self.mkdir("build_san")
		self.cd("build_san")
		
		self.run('cmake .. -GNinja '
			'-DCMAKE_BUILD_TYPE=Release '
			F'-DCMAKE_INSTALL_PREFIX={self.llvm_install_dir.joinpath("lib/clang/17")} '
			'-DCMAKE_C_COMPILER=x86_64-w64-mingw32-clang '
			'-DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-clang++ '
			'-DCMAKE_SYSTEM_NAME=Windows '
			F'-DCMAKE_AR={self.llvm_install_dir.joinpath("bin/llvm-ar")} '
			F'-DCMAKE_RANLIB={self.llvm_install_dir.joinpath("bin/llvm-ranlib")} '
			'-DCMAKE_C_COMPILER_WORKS=1 '
			'-DCMAKE_CXX_COMPILER_WORKS=1 '
			'-DCMAKE_C_COMPILER_TARGET=x86_64-w64-windows-gnu '
			'-DCOMPILER_RT_DEFAULT_TARGET_ONLY=TRUE '
			'-DCOMPILER_RT_USE_BUILTINS_LIBRARY=TRUE '
			'-DCOMPILER_RT_BUILD_BUILTINS=FALSE '
			'-DLLVM_CONFIG_PATH= '
			F'-DCMAKE_FIND_ROOT_PATH={self.llvm_install_dir.joinpath("x86_64-w64-mingw32")} '
			'-DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY '
			'-DCMAKE_FIND_ROOT_PATH_MODE_PACKAGE=ONLY '
			'-DSANITIZER_CXX_ABI=libc++ '
			'-DCMAKE_C_FLAGS_INIT= '
			'-DCMAKE_CXX_FLAGS_INIT= '
		)
			
		# self.run(
		# 	'cmake '
		# 	'-G"Ninja" '
		# 	F'-DLLVM_DIR="{self.llvm_install_dir}" '
		# 	F'-DLLVM_CMAKE_DIR={str(self.llvm_source_dir.joinpath("llvm/cmake/modules"))} '
		# 	'-DCMAKE_BUILD_TYPE=Release '
		# 	F'-DCMAKE_INSTALL_PREFIX="{self.llvm_install_dir.joinpath("lib/clang/17")}" '
		# 	'-DCMAKE_C_COMPILER=x86_64-w64-mingw32-clang '
		# 	'-DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-clang++ '
		# 	'-DCMAKE_SYSTEM_NAME=Windows '
		# 	F'-DCMAKE_AR="{self.llvm_install_dir.joinpath("bin/llvm-ar")}" '
		# 	F'-DCMAKE_RANLIB="{self.llvm_install_dir.joinpath("bin/llvm-ranlib")}" '
		# 	'-DCMAKE_C_COMPILER_WORKS=1 '
		# 	'-DCMAKE_CXX_COMPILER_WORKS=1 '
		# 	'-DCMAKE_C_COMPILER_TARGET=x86_64-w64-windows-gnu '
		# 	'-DLIBCXXABI_ENABLE_SHARED=OFF '
		# 	'-DLIBUNWIND_ENABLE_SHARED=OFF '
		# 	'-DCOMPILER_RT_ENABLE_STATIC_UNWINDER=ON '
		# 	'-DCOMPILER_RT_STATIC_CXX_LIBRARY=ON '
		# 	'-DDEFAULT_SANITIZER_USE_STATIC_CXX_ABI=ON '
		# 	'-DDEFAULT_SANITIZER_USE_STATIC_LLVM_UNWINDER=ON '
		# 	'-DSANITIZER_USE_STATIC_CXX_ABI=ON '
		# 	'-DSANITIZER_USE_STATIC_LLVM_UNWINDER=ON '
		# 	'-DDEFAULT_SANITIZER_USE_STATIC_TEST_CXX=ON '
		# 	'-DSANITIZER_USE_STATIC_TEST_CXX=ON '
		# 	'-DCOMPILER_RT_DEFAULT_TARGET_ONLY=TRUE '
		# 	'-DCOMPILER_RT_USE_BUILTINS_LIBRARY=TRUE '
		# 	'-DCOMPILER_RT_BUILD_BUILTINS=TRUE '
		# 	'-DLLVM_CONFIG_PATH="" '
		# 	F'-DCMAKE_FIND_ROOT_PATH={self.llvm_install_dir.joinpath("x86_64-w64-mingw32")} '
		# 	'-DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY '
		# 	'-DCMAKE_FIND_ROOT_PATH_MODE_PACKAGE=ONLY '
		# 	'-DSANITIZER_CXX_ABI=libc++ '
		# 	'-DCMAKE_C_FLAGS_INIT="-mguard=cf" '
		# 	'-DCMAKE_CXX_FLAGS_INIT="-mguard=cf" '
		# 	'../lib/builtins'
		# )
		self.run("ninja")
		self.run("ninja install")
		
		# self.run(F'mv -v {self.llvm_install_dir.joinpath("lib/clang/17/lib/windows/libclang_rt.asan_dynamic-x86_64.dll")} {self.llvm_install_dir.joinpath("x86_64-w64-mingw32/bin")}')
		os.environ["PATH"] = self.originalPATH

	def buildLLVMRuntimes(self):
		"""
		Build LLVM runtimes.
		"""
		self.cd(self.llvm_source_dir.joinpath("runtimes"))
		self.mkdir("build")
		self.cd("build")
		os.environ["PATH"] = F'{self.bin_dir}:{os.environ["PATH"]}'
		

		self.run("cmake .. -GNinja "
			"-DCMAKE_BUILD_TYPE=Release "
			F"-DCMAKE_INSTALL_PREFIX={self.llvm_install_dir.joinpath('x86_64-w64-mingw32')} "
			"-DCMAKE_C_COMPILER=x86_64-w64-mingw32-clang "
			"-DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-clang++ "
			"-DCMAKE_CXX_COMPILER_TARGET=x86_64-w64-windows-gnu "
			"-DCMAKE_SYSTEM_NAME=Windows "
			"-DCMAKE_C_COMPILER_WORKS=TRUE "
			"-DCMAKE_CXX_COMPILER_WORKS=TRUE "
			F"-DLLVM_PATH={self.llvm_source_dir.joinpath('llvm')} "
			F"-DCMAKE_AR={self.llvm_install_dir.joinpath('bin/llvm-ar')} "
			F"-DCMAKE_RANLIB={self.llvm_install_dir.joinpath('bin/llvm-ranlib')} "
			'-DLLVM_ENABLE_RUNTIMES="libunwind;libcxxabi;libcxx" '
			"-DLIBUNWIND_USE_COMPILER_RT=TRUE "
			"-DLIBUNWIND_ENABLE_SHARED=OFF "
			"-DLIBUNWIND_ENABLE_STATIC=ON "
			"-DLIBCXX_USE_COMPILER_RT=ON "
			"-DLIBCXX_ENABLE_SHARED=OFF "
			"-DLIBCXX_ENABLE_STATIC=ON "
			"-DLIBCXX_ENABLE_STATIC_ABI_LIBRARY=TRUE "
			"-DLIBCXX_CXX_ABI=libcxxabi "
			"-DLIBCXX_LIBDIR_SUFFIX= "
			"-DLIBCXX_INCLUDE_TESTS=FALSE "
			"-DLIBCXX_ENABLE_ABI_LINKER_SCRIPT=FALSE "
			"-DLIBCXXABI_USE_COMPILER_RT=ON "
			"-DLIBCXXABI_USE_LLVM_UNWINDER=ON "
			"-DLIBCXXABI_ENABLE_SHARED=OFF "
			"-DLIBCXXABI_LIBDIR_SUFFIX= "
			"-DCMAKE_C_FLAGS_INIT=-mguard=cf "
			"-DCMAKE_CXX_FLAGS_INIT=-mguard=cf "
		)



		# self.run("cmake .. "
		# 	"-GNinja "
		# 	"-DCMAKE_BUILD_TYPE=Release "
		# 	F"-DCMAKE_INSTALL_PREFIX={self.llvm_install_dir.joinpath('x86_64-w64-mingw32')} "
		# 	"-DCMAKE_C_COMPILER=x86_64-w64-mingw32-clang "
		# 	"-DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-clang++ "
		# 	"-DCMAKE_CXX_COMPILER_TARGET=x86_64-w64-windows-gnu "
		# 	"-DCMAKE_SYSTEM_NAME=Windows "
		# 	"-DCMAKE_C_COMPILER_WORKS=TRUE "
		# 	"-DCMAKE_CXX_COMPILER_WORKS=TRUE "
		# 	F"-DLLVM_PATH={self.llvm_source_dir.joinpath('llvm')} "
		# 	F"-DCMAKE_AR={self.llvm_install_dir.joinpath('bin/llvm-ar')} "
		# 	F"-DCMAKE_RANLIB={self.llvm_install_dir.joinpath('bin/llvm-ranlib')} "
		# 	'-DLLVM_ENABLE_RUNTIMES="libunwind;libcxxabi;libcxx" '
		# 	"-DLIBUNWIND_USE_COMPILER_RT=TRUE "
		# 	"-DLIBUNWIND_ENABLE_SHARED=OFF "
		# 	"-DLIBUNWIND_ENABLE_STATIC=ON "
		# 	"-DLIBCXX_USE_COMPILER_RT=ON "
		# 	"-DLIBCXX_ENABLE_SHARED=OFF "
		# 	"-DLIBCXX_ENABLE_STATIC=ON "
		# 	"-DLIBCXX_ENABLE_STATIC_ABI_LIBRARY=TRUE "
		# 	"-DLIBCXX_CXX_ABI=libcxxabi "
		# 	"-DLIBCXX_LIBDIR_SUFFIX= "
		# 	"-DLIBCXX_INCLUDE_TESTS=FALSE "
		# 	"-DLIBCXX_ENABLE_ABI_LINKER_SCRIPT=FALSE "
		# 	"-DLIBCXXABI_USE_COMPILER_RT=ON "
		# 	"-DLIBCXXABI_USE_LLVM_UNWINDER=ON "
		# 	"-DLIBCXXABI_ENABLE_SHARED=OFF "
		# 	'-DLIBCXXABI_LIBDIR_SUFFIX="" '
		# 	"-DCMAKE_C_FLAGS_INIT=-mguard=cf "
		# 	"-DCMAKE_CXX_FLAGS_INIT=-mguard=cf "
		# 	)

		self.run("ninja")
		self.run("ninja install")
		os.environ["PATH"] = self.originalPATH

	def buildMingwLibs(self):
		"""
		Build MinGW libraries.
		"""
		self.cd(self.mingw_source_dir.joinpath("mingw-w64-libraries"))
		os.environ["CFLAGS"] = "-g -O2 -mguard=cf"
		os.environ["CXXFLAGS"] = "-g -O2 -mguard=cf"
		os.environ["PATH"] = F'{self.bin_dir}:{os.environ["PATH"]}'
		self.cd("winpthreads")
		self.mkdir("build")
		self.cd("build")
		self.run(F'../configure --disable-shared --enable-static --host=x86_64-w64-mingw32 '
			F'--prefix={self.llvm_install_dir.joinpath("x86_64-w64-mingw32")} '
			F'--libdir={self.llvm_install_dir.joinpath("x86_64-w64-mingw32/lib")} '
			)
		self.run("make -j8")
		self.run("make install")

		self.cd("..")
		self.cd("..")
		self.cd("winpthreads")
		self.mkdir("build")
		self.cd("build")
		self.run(F'../configure --disable-shared --enable-static --host=x86_64-w64-mingw32 '
			F'--prefix={self.llvm_install_dir.joinpath("x86_64-w64-mingw32")} '
			F'--libdir={self.llvm_install_dir.joinpath("x86_64-w64-mingw32/lib")} '
			)
		self.run("make -j8")
		self.run("make install")

		self.cd(self.mingw_source_dir.joinpath("mingw-w64-libraries"))
		self.cd("winstorecompat")
		self.mkdir("build")
		self.cd("build")
		self.run(F'../configure --disable-shared --enable-static --host=x86_64-w64-mingw32 '
			F'--prefix={self.llvm_install_dir.joinpath("x86_64-w64-mingw32")} '
			F'--libdir={self.llvm_install_dir.joinpath("x86_64-w64-mingw32/lib")} '
			)
		self.run("make -j8")
		self.run("make install")
		os.environ["PATH"] = self.originalPATH

	def buildOpenMP(self):
		"""
		Build OpenMP runtime.
		"""
		os.environ["PATH"] = F'{self.bin_dir}:{os.environ["PATH"]}'
		# os.environ["LLVM_DIR"] = str(self.llvm_source_dir.joinpath("llvm").joinpath("build"))
		self.cd(self.llvm_source_dir.joinpath("openmp"))
		self.mkdir("build")
		self.cd("build")

		self.run("cmake .. -GNinja "
		"-DCMAKE_BUILD_TYPE=Release "
		F"-DCMAKE_INSTALL_PREFIX={self.llvm_install_dir.joinpath('x86_64-w64-mingw32')} "
		"-DCMAKE_C_COMPILER=x86_64-w64-mingw32-clang "
		"-DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-clang++ "
		"-DCMAKE_RC_COMPILER=x86_64-w64-mingw32-windres "
		"-DCMAKE_ASM_MASM_COMPILER=llvm-ml "
		"-DCMAKE_SYSTEM_NAME=Windows "
		F'-DCMAKE_AR="{self.llvm_install_dir.joinpath("bin/llvm-ar")}" '
		F'-DCMAKE_RANLIB="{self.llvm_install_dir.joinpath("bin/llvm-ranlib")}" '
		"-DLIBOMP_ENABLE_SHARED=FALSE "
		"-DCMAKE_C_FLAGS_INIT=-mguard=cf "
		"-DCMAKE_CXX_FLAGS_INIT=-mguard=cf "
		"-DLIBOMP_ASMFLAGS=-m64 "
		)

		# self.run("cmake .. "
		# 	"-G Ninja "
		# 	"-DCMAKE_INSTALL_PREFIX:PATH=../../../../x86_64-w64-mingw32 "
		# 	"-DCMAKE_BUILD_TYPE=Release "
		# 	"-DCMAKE_C_COMPILER=x86_64-w64-mingw32-clang "
		# 	"-DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-clang++ "
		# 	"-DCMAKE_C_COMPILER_TARGET=x86_64-w64-windows-gnu "
		# 	"-DCMAKE_C_COMPILER_WORKS=TRUE "
		# 	"-DCMAKE_CXX_COMPILER_WORKS=TRUE "
		# 	"-DCMAKE_C_FLAGS_INIT=-mguard=cf "
		# 	"-DCMAKE_CXX_FLAGS_INIT=-mguard=cf "
		# 	"-DOPENMP_ENABLE_LIBOMPTARGET=0 "
		# 	"-DLIBOMP_ARCH=x86_64-w64-mingw32 "
		# 	"-DCMAKE_AR=../../../../bin/llvm-ar "
		# 	"-DCMAKE_RANLIB=../../../../bin/llvm-ranlib "
		# 	)
		
		# self.run("cmake .. "
		# 	"-G Ninja "
		# 	"-DCMAKE_BUILD_TYPE=Release "
		# 	F'-DCMAKE_INSTALL_PREFIX="{self.llvm_install_dir.joinpath("x86_64-w64-mingw32")}" '
		# 	"-DCMAKE_C_COMPILER=x86_64-w64-mingw32-clang "
		# 	"-DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-clang++ "
		# 	"-DCMAKE_RC_COMPILER=x86_64-w64-mingw32-windres "
		# 	"-DCMAKE_ASM_MASM_COMPILER=llvm-ml "
		# 	"-DCMAKE_SYSTEM_NAME=Windows "
		# 	F'-DCMAKE_AR="{self.llvm_install_dir.joinpath("bin/llvm-ar")}" '
		# 	F'-DCMAKE_RANLIB="{self.llvm_install_dir.joinpath("bin/llvm-ranlib")}" '
		# 	"-DLIBOMP_ENABLE_SHARED=FALSE "
		# 	'-DCMAKE_C_FLAGS_INIT="-mguard=cf" '
		# 	'-DCMAKE_CXX_FLAGS_INIT="-mguard=cf" '
		# 	"-DLIBOMP_ASMFLAGS=-m64 "
		# )
		self.run("ninja")
		self.run("ninja install")
		os.environ["PATH"] = self.originalPATH

	def symlinkGCCEH(self):
		self.cd(self.llvm_install_dir.joinpath('x86_64-w64-mingw32/lib'))
		self.sn("libunwind.a", "libgcc_eh.a")
		self.sn(self.llvm_install_dir.joinpath("lib/clang/17/lib/windows/libclang_rt.builtins-x86_64.a"), "libgcc.a")

	def createUnwindPC(self):
		self.mkdir(self.llvm_install_dir.joinpath('x86_64-w64-mingw32/lib/pkgconfig/'))
		pcfile = F"prefix={self.llvm_install_dir.joinpath('x86_64-w64-mingw32/x86_64-w64-mingw32')}\n" \
			'exec_prefix=${prefix}\n' \
			'libdir=${prefix}/lib\n' \
			'includedir=${prefix}/include\n' \
			'\n' \
			'Name: libunwind\n' \
			'Description: libunwind base library\n' \
			'Version: 1.7.2\n' \
			'Libs: -L${libdir} -lunwind\n' \
			'Libs.private: -llzma -lz\n' \
			'Cflags: -I${includedir}\n'
		with open(self.llvm_install_dir.joinpath('x86_64-w64-mingw32/lib/pkgconfig/libunwind.pc'), "w") as f:
			f.write(pcfile)




if __name__ == "__main__":
	installer = LLVMInstaller()
	installer.build()