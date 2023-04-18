
from packages.base_package import BasePackage


class libarchive(BasePackage):
    name = "libarchive"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        self.patches = [
            {"file":'libarchive/0001-libarchive-mingw-workaround.patch'}
        ]
        self.regex_replace = {
            "post_install": [
                {
                    0: r"Libs.private:  -lz -lbz2 -llzma -llzo2 -lcrypto -liconv -lcharset -lexpat\n",
                    1: r"Libs.private:  -lz -lbz2 -llzma -llzo2 -lcrypto -lbcrypt -ltls -lws2_32 -liconv -lcharset -lexpat\n",
                    "in_file": "{pkg_config_path}/libarchive.pc",
                },
            ]
        }

    @property
    def pkg_depends(self):
        return ['bzip2', 'expat', 'zlib', 'lzma', "libxml2", 'lzo',]

    @property
    def pkg_url(self) -> str:
        return "https://github.com/libarchive/libarchive.git"

    @property
    def pkg_config(self):
        return (
            "..",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DBUILD_SHARED_LIBS=OFF",
			'-DENABLE_NETTLE=ON',
			'-DENABLE_OPENSSL=ON',
			'-DENABLE_LIBB2=ON',
			'-DENABLE_LZ4=ON',
			'-DENABLE_LZO=ON',
			'-DENABLE_LZMA=ON',
			'-DENABLE_ZSTD=ON',
			'-DENABLE_ZLIB=ON',
			'-DZLIB_WINAPI_EXITCODE=0',
			'-DZLIB_WINAPI_EXITCODE_TRYRUN_OUTPUT=""',
			'-DENABLE_BZip2=ON',
			'-DENABLE_LIBXML2=OFF',
			'-DENABLE_EXPAT=ON',
			'-DENABLE_LibGCC=ON',
			'-DENABLE_CNG=ON',
			'-DENABLE_TAR=OFF',
			'-DENABLE_TAR_SHARED=OFF',
			'-DENABLE_CPIO=OFF',
			'-DENABLE_CPIO_SHARED=OFF',
			'-DENABLE_CAT=ON',
			'-DENABLE_CAT_SHARED=OFF',
			'-DENABLE_XATTR=ON',
			'-DENABLE_ACL=ON',
			'-DENABLE_ICONV=ON',
			'-DENABLE_TEST=OFF',
			'-DENABLE_COVERAGE=OFF',
		    # '-DLIBXML2_LIBRARIES=-lxml2 -lz -llzma -liconv -lws2_32',
            # '-DOPENSSL_CRYPTO_LIBRARY=!CMD(pkg-config --static libcrypto --libs-only-l)CMD!',
            # '-DOPENSSL_LIBRARIES=!CMD(pkg-config --static openssl --libs-only-l)CMD!',
            # '-DBZIP2_LIBRARIES=!CMD(pkg-config --static bzip2 --libs-only-l)CMD!',
			# '-DLIBXML2_LIBRARIES=!CMD(pkg-config --static libxml-2.0 --libs-only-l)CMD!',
            #-lxml2 -lz -llzma -liconv -lws2_32
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]

