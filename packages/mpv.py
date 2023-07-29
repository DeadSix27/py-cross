from packages.base_package import BasePackage


class mpv(BasePackage):
    name = "mpv"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Meson
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"

        self.patches = [
            {"file": "mpv/ádd-lib-prefix.patch"},
            # ( 'https://github.com/mpv-player/mpv/pull/11494.patch', '-p1'), # win32: add an option to change window affinity #11494 
            # {"file": "https://github.com/mpv-player/mpv/pull/11552.patch"}, #  win32: add window transparency option #11552
            # {"file": "https://github.com/mpv-player/mpv/pull/9975.patch" },
            # {"file": "mpv/0001-change-icons.patch", "cmd": "git apply "  },
            # {"file": "https://github.com/mpv-player/mpv/pull/11574.patch"},
            {"file": "https://github.com/mpv-player/mpv/pull/11650.patch"},
            # {"file": "https://github.com/mpv-player/mpv/pull/11971.patch"},
            {"file": "https://github.com/mpv-player/mpv/pull/10316.patch"},
            
        ]

        self.regex_replace = {
            "post_download": [
                {
                    0: r"\"--dirty\"",  # dirty.
                    1: r"",
                    "in_file": "version.py",
                },
                {
                    0: r"bool encoder_encode",
                    1: r"bool mpv_encoder_encode",
                    "in_file": "common/encode_lavc.c",
                },
                {
                    0: r"bool encoder_encode",
                    1: r"bool mpv_encoder_encode",
                    "in_file": "common/encode_lavc.h",
                },
                {
                    0: r"encoder_encode",
                    1: r"mpv_encoder_encode",
                    "in_file": "video/out/vo_lavc.c",
                },
                {
                    0: r"encoder_encode",
                    1: r"mpv_encoder_encode",
                    "in_file": "audio/out/ao_lavc.c",
                },
            ],
        }

    @property
    def pkg_depends(self):
        return [
            "libffmpeg",
            "zlib",
            "iconv",
            "python",
            "vapoursynth",
            # "caca",
            "sdl2",
            "luajit",
            'rubberband',
            "lcms2",
            "libdvdnav",
            "openal",
            "libbluray",
            "openal",
            "libass",
            "libcdio-paranoia",
            "libjpeg_turbo",
            "uchardet",
            "libarchive",
            "mujs",
            "shaderc",
            "vulkan-loader",
            "libplacebo",
            "zimg",
        ]

    def post_install_commands(self):
        self.compiler.runProcess(
            ["{mingw_prefix_dash}strip", "-v", "{install_path}/mpv/bin/mpv.com"]
        )
        self.compiler.runProcess(
            ["{mingw_prefix_dash}strip", "-v", "{install_path}/mpv/bin/mpv.exe"]
        )
        self.compiler.runProcess(
            ["{mingw_prefix_dash}strip", "-v", "{install_path}/mpv/bin/mpv-2.dll"]
        )

    @property
    def pkg_url(self):
        return "https://github.com/mpv-player/mpv.git"

    @property
    def pkg_config(self):
        return [
            "..",
            "{meson_options}",
            "--default-library=static",
            "--prefix={install_path}/mpv",
            "--default-library=both",
            "--backend=ninja",
            "-Dcdda=enabled",
            # '-Ddvbin=enabled',
            "-Ddvdnav=enabled",
            "-Diconv=enabled",
            "-Djavascript=enabled",
            "-Dlcms2=enabled",
            "-Dlibarchive=enabled",
            "-Dlibavdevice=enabled",
            "-Dlibbluray=enabled",
            "-Dlua=enabled",
            "-Dcplayer=true",
            "-Drubberband=enabled",
            "-Dsdl2=enabled",
            "-Dsdl2-gamepad=enabled",
            "-Dsdl2-audio=enabled",
            "-Dvapoursynth=enabled",
            "-Dlibplacebo-next=enabled",
            "-Dmanpage-build=disabled",
            "-Dhtml-build=enabled",
            # "-Dpdf-build=disabled",
            "-Dzimg=enabled",
            "-Dzlib=enabled",
            "-Dopenal=enabled",
            # "-Dcaca=enabled",
            "-Ddirect3d=enabled",
            # '-Degl-angle-win32=enabled ',
            "-Dlibrary-prefix=",
            "-Dgl-dxinterop=enabled",
            "-Dgl-win32=enabled",
            "-Dlibmpv=true",
            "-Doptimization=3",
            # "-Dpython=enabled",
        ]

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]