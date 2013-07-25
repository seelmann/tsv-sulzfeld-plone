# -*- extra stuff goes here -*-


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    # Register additional easytemplat tags
    from tsv.policy.easytemplate.tags import TodayTag, SpieltermineTag, VereinstermineTag
    tags = [TodayTag(), SpieltermineTag(), VereinstermineTag()] 
    from collective.easytemplate import tagconfig
    [tagconfig.tags.append(tag) for tag in tags]
    from collective.easytemplate.engine import getEngine, setupEngine
    from collective.templateengines.backends import jinja
    [getEngine().addTag(tag) for tag in tags]
    setupEngine(jinja.Engine())

