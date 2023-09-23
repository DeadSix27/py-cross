from packages.base_package import BasePackage


class LIBFFMPEG(BasePackage):
    name = "libffmpeg"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
        # self.git_tag = "639ded10e3599b7dd52a4bd7c06589689d177d08"
        # self.patches = [
            # {"file": "https://github.com/FFmpeg/FFmpeg/commit/02aeacbb5e77f1c760031dc6426a46671c6d220a.patch", "cmd": "patch -p1 -R"},
        # ]
        # self.git_branch = "vulkan"

    @property
    def pkg_depends(self):
        return (
            "shine",
            # "libssh",
            "avisynth",
            "bzip2",
            "frei0r",
            "libass",
            "libbluray",
            # "libbs2b",
            # "caca",
            "dav1d",
            # "xavs",
            # "libressl",
            "opencl_icd",
            "openssl",
            # "xavs2",
            # "davs2",
            "fdkaac",
            "gme",
            "gsm",
            "libilbc",
            "libjxl",
            "kvazaar",
            "lensfun",
            "mfx",
            "libmodplug",
            "libmysofa",
            "opencore_amr",
            "openh264",
            "openjpeg",
            "lcms2",
            "openmpt",
            "libplacebo",
            "rav1e",
            "rtmpdump",
            "libsamplerate",
            "freetype2",
            "rubberband",
            "snappy",
            "soxr",
            "srt",
            "svt-av1",
            "svt-vp9",
            "svt-hevc",
            "tesseract",
            "theora",
            "vidstab",
            "vo_amrwbenc",
            "libvpx",
            "x264",
            "x265",
            "xvidcore",
            "zimg",
            "zvbi",
            "aom",
            "twolame",
            "zvbi",
            "openal",
            "vapoursynth",
            "libcdio-paranoia",
            "nv-codec-headers",
            "amf",
        )
    @property
    def pkg_env(self):
        return {
            "OPENAL_LIBS": "-lOpenAL32 -lstdc++ -lwinmm -lole32",
        }
    @property
    def pkg_url(self):
        return "https://github.com/FFmpeg/FFmpeg"
        # return "https://github.com/cyanreg/FFmpeg"

    @property
    def pkg_config(self):
        return (
            "--sysroot={toolchain_path_one}",
            "--arch={arch_string}",
            "--target-os=mingw32",
            "--cross-prefix={mingw_prefix_dash}",
            "--pkg-config=pkg-config",
            "--pkg-config-flags=--static",
            "--disable-w32threads",
            "--enable-cross-compile",
            "--target-exec=wine",
            "--enable-runtime-cpudetect",
            "--enable-gpl",
            "--enable-version3",
            "--extra-version=xcompile",
            # Misc.
            "--enable-lcms2",
            "--enable-pic",
            "--enable-bzlib",
            "--enable-zlib",
            "--enable-lzma",
            # '--enable-gcrypt',
            "--enable-fontconfig",
            "--enable-libfontconfig",
            "--enable-libfreetype",
            "--enable-libfribidi",
            "--enable-libbluray",
            "--enable-libcdio",
            "--enable-avisynth",
            "--enable-vapoursynth",  # maybe works?
            "--enable-librtmp",
            # "--enable-libcaca",
            "--enable-iconv",
            "--enable-libxml2",
            # '--enable-gmp',
            "--enable-openssl",
            # "--enable-libtls",
            # '--enable-gnutls', # nongpl: openssl,libtls(libressl)
            "--enable-vulkan",
            "--enable-libshaderc",
            "--enable-libplacebo",
            # Video/Picture Libs
            "--enable-libzimg",
            "--enable-libx264",
            "--enable-libopenh264",
            "--enable-libx265",
            # "--enable-libkvazaar",
            "--enable-libvpx",
            "--enable-libdav1d",
            "--enable-libaom",
            "--enable-libsvtav1",
            "--enable-librav1e",
            "--enable-libxvid",
            "--enable-gray",
            # Audio Libs
            "--enable-libshine",
            # "--enable-libssh",
            "--enable-libopus",
            "--enable-libmp3lame",
            "--enable-libvorbis",
            "--enable-libtheora",
            "--enable-libspeex",
            "--enable-libsoxr",
            "--enable-librubberband",
            "--enable-openal",
            # Subtitle/OCR Libs:
            "--enable-libass",
            "--enable-libtesseract",
            "--enable-liblensfun",
            # Image libs
            "--enable-libwebp",
            "--enable-libopenjpeg",
            "--enable-libjxl",
            # HW Decoders
            "--enable-ffnvcodec",
            "--enable-cuvid",
            "--enable-opengl",
            "--enable-opencl",
            "--enable-d3d11va",
            "--enable-nvenc",
            "--enable-nvdec",
            "--enable-dxva2",
            "--enable-cuda-nvcc",
            "--enable-libmfx",
            "--enable-amf",
            "--extra-cflags=-DAL_LIBTYPE_STATIC -DMODPLUG_STATIC",
            "--enable-libtwolame",
            "--enable-libzvbi",
            "--enable-libgsm",
            "--enable-libopencore-amrnb",
            "--enable-libopencore-amrwb",
            "--enable-libvo-amrwbenc",
            "--enable-libsnappy",
            "--enable-frei0r",
            "--enable-filter=frei0r",
            "--enable-libsrt",
            # "--enable-libbs2b",
            "--enable-libilbc",
            "--enable-libgme",
            #'--enable-libflite', #todo fix this shit
            "--enable-sdl",
            # "--enable-libdavs2",
            # "--enable-libxavs",
            # "--enable-libxavs2",
            "--enable-libopenmpt",
            "--enable-libmysofa",
            "--enable-libvidstab",
            "--enable-libmodplug",
            # '--disable-schannel '
            #'--disable-gcrypt '
            #'--enable-ladspa '
            # '--enable-libcodec2 ' # Requires https://github.com/traviscross/freeswitch/tree/master/libs/libcodec2, too lazy to split that off.
            # '--enable-libvmaf '
            # '--extra-libs="-lpsapi" '
            # '--extra-libs="-liconv" ' # -lschannel #-lsecurity -lz -lcrypt32 -lintl -liconv -lpng -loleaut32 -lstdc++ -lspeexdsp -lpsapi
            # '--extra-cflags="-DLIBTWOLAME_STATIC" '
            # '--extra-cflags="-DMODPLUG_STATIC" '
            "--enable-nonfree",
            "--enable-libfdk-aac",
            # '--enable-decklink',
            # --enable-cuda-sdk # nonfree stuff
            "--prefix={target_prefix}",
            "--disable-sdl2",
            "--disable-shared",
            "--enable-static",
            "--disable-doc",
            "--disable-programs",
            "--disable-doc",
            "--disable-htmlpages",
            "--disable-manpages",
            "--disable-podpages",
            "--disable-txtpages",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]
