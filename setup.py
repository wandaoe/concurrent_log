import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="huanghyw", # Replace with your own username
    version="0.0.1",
    author="HuangYiwei",
    author_email="huanghyw@gmail.com",
    description="多进程并发日志处理器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huanghyw/concurrent_log",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)