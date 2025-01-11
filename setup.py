from setuptools import setup, find_packages

setup(
    name='ChinesePatentParser',  # Replace with your package name
    version='1.0',               # Version of your package
    author='Mark Gu',            # Your name
    author_email='mark.reachee@gmail.com', # Your email
    description='A Python script that can parse a Chinese patent of invention type to extract fields, sections, and subsections in it.',
    long_description=open('README.md').read(), # Read long description from README
    long_description_content_type='text/markdown',
    url='https://github.com/msmarkgu/ChinesePatentParser', # Your package URL
    packages=find_packages(),             # Automatically find packages
    install_requires=[                    # List of dependencies
        'pdfplumber'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # Adjust as necessary
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',              # Minimum Python version
)
