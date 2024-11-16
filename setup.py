from setuptools import setup, find_packages

setup(
    name="git-contribution-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "gitpython>=3.1.0",
        "requests>=2.25.1",
        "python-dotenv>=0.19.0",
        "pyyaml>=5.4.1",
        "beautifulsoup4>=4.9.3",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "git-analyzer=src.core.contribution_analyzer:main",
        ],
    },
)
