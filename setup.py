import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
    'console_scripts': [
    ],
}

TESTS_REQUIRE = [
    'fudge',
    'nose',
    'nose-timer',
    'nose-pudb',
    'nose-progressive',
    'nose2[coverage_plugin]',
    'pyhamcrest',
    'nti.nose_traceback_info',
    'nti.testing',
]

setup(
	name='nti.analytics_pandas',
	version=VERSION,
	author='Josh Zuech',
	author_email='josh.zuech@nextthought.com',
	description="NTI Analytics Pandas",
	long_description=codecs.open('README.rst', encoding='utf-8').read(),
	license='Proprietary',
	keywords='Analytics Pandas',
	classifiers=[
		'Intended Audience :: Developers',
		'Natural Language :: English',
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.2",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: Implementation :: CPython",
	],
	packages=find_packages('src'),
	package_dir={'': 'src'},
	namespace_packages=['nti'],
	install_requires=[
        'setuptools',
        'lxml',
        'matplotlib',
        'numpy',
        'pandas',
        'pymysql',
        'pypdf2',
        'pygal',
        'user_agents',
        'sqlalchemy',
        'zope.component',
        'zope.event',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.location',
        'zope.proxy',
        'zope.schema',
        'zope.security',
        'nti.analytics_database',
        'nti.common'
	],
	tests_require=TESTS_REQUIRE,
	entry_points=entry_points,
	extras_require={
        'test': TESTS_REQUIRE,
        'tools': [
			'epydoc',	# auto-api docs
			'httpie',
			'ipython',
			'logilab_astng',
			'pip',
			'pudb',
			'pylint',  # install astroid
			'readline',
			'rope',
			'ropemode',
			'virtualenv',
			'virtualenvwrapper',
			'z3c.dependencychecker',
			'Babel',
			'lingua',
		]
    },
    test_suite='nose2.compat.unittest.collector'
)
