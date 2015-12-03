import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
	'console_scripts': [
		'nti_analytics_assesments = nti.analytics_pandas.reports.scripts.assessments:main',
		'nti_analytics_bookmarks = nti.analytics_pandas.reports.scripts.bookmarks:main',
		'nti_analytics_enrollments = nti.analytics_pandas.reports.scripts.enrollments:main',
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
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: Implementation :: CPython",
	],
	packages=find_packages('src'),
	package_dir={'': 'src'},
	namespace_packages=['nti'],
	install_requires=[
		'setuptools',
		# 'ggplot',
		'lxml',
		'matplotlib',
		'numpy',
		'pandas',
		'pymysql',
		'pypdf2',
		'pytz',
		'reportlab',
		# 'scipy', required by ggplot, does not work very well with buildout
		'sqlalchemy',
		'user_agents',
		'z3c.rml',
		'z3c.macro',
		'z3c.pagelet',
		'z3c.pt',
		'z3c.ptcompat',
		'z3c.template',
		'zope.browserpage',
		'zope.component',
		'zope.contentprovider',
		'zope.event',
		'zope.i18nmessageid',
		'zope.interface',
		'zope.location',
		'zope.proxy',
		'zope.schema',
		'zope.security',
		'zope.tal',
		'zope.tales',
		'zope.viewlet',
		'nti.analytics_database',
		'nti.common',
		'nti.schema'
	],
	tests_require=TESTS_REQUIRE,
	entry_points=entry_points,
	extras_require={
		'test': TESTS_REQUIRE,
		'tools': [
			'epydoc',  # auto-api docs
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
