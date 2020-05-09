from setuptools import find_packages, setup

setup(
    name="boosearch",
    version="0.0.1",
    packages=find_packages(),
    description="Goofy boolean search and indexing",
    python_requires=">=3.5.0",
    install_requires=[
        "Click>=7.0",
        "importlib_resources ; python_version<'3.7'",
        "pymorphy2[fast]",
        "ujson",
        "sympy",
        "tqdm",
        "transformers",
        "torch",
    ],
    entry_points={"console_scripts": ["boos = boosearch.cli:main"]},
    zip_safe=True,
    include_package_data=True,
)
