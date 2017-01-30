"""
Transcript Models

"""
from schematics.models import Model
from schematics.types import StringType, DateTimeType, BooleanType, IntType
from schematics.types.compound import ListType, ModelType
from schematics.types.serializable import serializable


class Person(Model):
	name = StringType()
	party = StringType()
	state = StringType()
	relation = StringType()

	@serializable
	def disambiguous(self):
		parts = self.name.split(' ')
		if len(parts) > 1:
			return '{0}. {1}'.format(self.name[0:1], self.surname)
		return self.surname

	@serializable
	def surname(self):
		return self.name.split(' ')[-1]


class Dialog(Model):
	person = ModelType(Person)
	speech = StringType()
	timestamp = DateTimeType()
	videoclip = BooleanType(default=False)


class VideoDialog(Model):
	person = ModelType(Person)
	speech = StringType()
	timestamp = DateTimeType()
	sequence = IntType(default=0)


class Video(Model):
	description = StringType()
	airdate_start = DateTimeType()
	airdate_end = DateTimeType()
	transcript = ListType(ModelType(VideoDialog), default=[])
	sequence = IntType(default=0)
	length = IntType(default=0)


class Show(Model):
	name = StringType()
	keyword = StringType()
	headlines = StringType()
	airdate_start = DateTimeType()
	airdate_end = DateTimeType()
	transcript = ListType(ModelType(Dialog), default=[])
	videos = ListType(ModelType(Video), default=[])
	people = ListType(ModelType(Person), default=[])

