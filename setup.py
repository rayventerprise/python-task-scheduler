"""
Setup script for Distributed Task Scheduler
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="distributed-task-scheduler",
    version="0.1.0",
    author="Ray",
    author_email="ray@venterprise.io",
    description="A low-level, asyncio-based distributed task scheduler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rayventerprise/distributed-task-scheduler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    entry_points={
        "console_scripts": [
            "dts-server=server:main",
            "dts-worker=worker:main",
            "dts-client=client:main",
        ],
    },
    keywords="distributed computing, asyncio, task scheduler, rpc",
    project_urls={
        "Bug Reports": "https://github.com/rayventerprise/distributed-task-scheduler/issues",
        "Source": "https://github.com/rayventerprise/distributed-task-scheduler",
        "Documentation": "https://github.com/rayventerprise/distributed-task-scheduler#readme",
    },
) 