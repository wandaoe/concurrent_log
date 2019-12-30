import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = ['portalocker>=1.5.2']

setuptools.setup(
    name="concurrent_log",
    version="1.0.1",
    author="HuangYiwei",
    author_email="huanghyw@gmail.com",
    description="多进程并发日志处理器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    url="https://github.com/huanghyw/concurrent_log",
    packages=['concurrent_log'],
    package_dir={'': 'src', },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)