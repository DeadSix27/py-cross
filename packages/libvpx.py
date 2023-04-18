from packages.base_package import BasePackage


class libvpx(BasePackage):
    name = "libvpx"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

        self.patches = [
            {"file": 'vpx/vpx_160_semaphore.patch' }
        ]

        # 'env_exports' : {
        # 	'CROSS' : '{cross_prefix_bare}',
        # },
        # 'cflag_addition' : '-fno-asynchronous-unwind-tables',
        # 'patches' : [
        # 	( '', '-p1' ),
        # ],


    @property
    def pkg_env(self):
        return {
            "CFLAGS": "-fno-asynchronous-unwind-tables",
            "CROSS": "{mingw_prefix_dash}",
        }

    @property
    def pkg_depends(self):
        return ()

    @property
    def pkg_url(self) -> str:
        return "https://chromium.googlesource.com/webm/libvpx"

    @property
    def pkg_config(self):
        return (
            "--disable-shared",
            "--enable-static",
            # "--build=x86_64-pc-linux-gnu",
            "--target={bitness}-{bitness_win}-gcc",
            "--prefix={target_prefix}",
            "--enable-webm-io",
            "--enable-libyuv",
            "--enable-vp9",
            "--enable-vp8",
            "--enable-runtime-cpu-detect",
            "--enable-postproc",
            "--enable-vp9-highbitdepth",
            "--enable-vp9-postproc",
            # "--enable-coefficient-range-checking",
            "--enable-postproc-visualizer",
            "--enable-error-concealment",
            "--enable-better-hw-compatibility",
            "--enable-multi-res-encoding",
            "--enable-vp9-temporal-denoising",
            "--disable-tools",
            "--disable-docs",
            "--disable-examples",
            "--disable-install-docs",
            "--disable-unit-tests",
            "--disable-decode-perf-tests",
            "--disable-encode-perf-tests",
            "--as=yasm",
    )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "libvpx"}