from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator


class KeystonesAggregator(AbstractAggregator):

    def get_output(self) -> (str, str):
        return 'Keystones', self._get_keystones(self.build.keystones)

    @staticmethod
    def _get_keystones(keystones: list, minified=False):
        keystones = [keystone['name'] if not minified else keystone['abbrev'] for keystone in keystones]
        return ", ".join(keystones)
