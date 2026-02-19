from setuptools import setup, find_packages

setup(
    name="openclaw",
    version="0.1.0",
    description="AI Assistant Creation Networking Platform",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
)
