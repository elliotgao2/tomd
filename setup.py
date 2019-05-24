from setuptools import find_packages, setup

setup(
    name="tomd",
    version="0.1.4",
    description="Convert HTML to Markdown.",
    author="Gaojiuli",
    author_email="gaojiuli@gmail.com",
    url='https://github.com/gaojiuli/tomd',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'pyquery'
    ],
    license='GNU GPL 3',
    packages=find_packages(),
    py_modules=['tomd'],
    include_package_data=True,
    zip_safe=False,
)
