from setuptools import setup


setup(
    name="evilemu",
    description="A python library to access rom/ram memory of running emulators, without their cooperation.",
    author="Daid",
    url="https://github.com/daid/pyevilemu",
    project_urls={
        "Issues": "https://github.com/daid/pyevilemu/issues",
        "CI": "https://github.com/daid/pyevilemu/actions",
        "Changelog": "https://github.com/daid/pyevilemu/releases",
    },
    license="MIT License",
    version="0.1",
    packages=["evilemu", "evilemu.win"],
    install_requires=[],
    python_requires=">=3.7",
)
