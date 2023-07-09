from setuptools import setup, find_packages
import glob
from os import path

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

script_files = glob.glob('src/*.py')
other_files = glob.glob('')
script_files.extend(other_files)

#script_files = glob.glob('')

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='gpterm-tool',
    version='0.0.2',
    packages=find_packages('src'),
    license='MIT',
    description = 'Creating Intelligent Terminal Apps with ChatGPT and LLM Models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'A.Akdogan',                   
    author_email = 'adem.akdogan92@gmail.com',      
    url = 'https://github.com/ademakdogan/GPTerm',    
    keywords = ['CHATGPT', 'NLP', 'LLM', 'TERMINAL'],  
    #scripts=['src/alpaca.py',
    #         'src/gpterm.py',
    #         'src/llm_writer.py',
    #         'src/responser.py',
    #         'src/utils.py'],
    scripts = script_files,
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'GPTerm = gpterm:main',
        ],
    },
    install_requires=requirements,
)


