from setuptools import find_packages, setup

_version = '0.1.4'

setup(
    name='vicore',
    version=_version,
    description='vial-core (vicore), a reusable vial architecture core module',
    packages=find_packages(),
    author='Chia Jason',
    author_email='chia_jason96@live.com',
    url='https://github.com/toranova/vicoreibase/',
    download_url='https://github.com/ToraNova/vicoreibase/archive/refs/tags/v%s.tar.gz' % _version,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    keywords = ['Flask'],
    install_requires=[
        'flask',
        'sqlalchemy',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
