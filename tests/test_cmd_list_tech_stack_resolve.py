import csv
from types import SimpleNamespace

from typer.testing import CliRunner

from banshee.commands.cmd_lists import app

runner = CliRunner()


def test_list_tech_stack_resolve_requires_args():
    result = runner.invoke(app, args=['tech-stack-resolve'])
    assert result.exit_code == 2


def test_list_tech_stack_resolve_generates_csv(monkeypatch, tmp_path):
    infile = tmp_path / 'stack.csv'
    infile.write_text('Cisco Nexus 9000 Series\nSome Cool Technology Dude\nNo Match Product\n')

    outfile = tmp_path / 'out.csv'

    found = lambda entity, entity_id, type_: SimpleNamespace(  # noqa: E731
        is_found=True,
        entity=entity,
        content=SimpleNamespace(id_=entity_id, type_=type_),
    )

    class FakeEntityMatchMgr:
        def match(self, name, type_, limit):
            assert type_ == ['Product', 'ProductIdentifier']
            assert limit == 3

            if name == 'Cisco Nexus 9000 Series':
                return [found('Cisco Nexus 9000', 'prod-1', 'Product')]

            if name == 'Some Cool Technology Dude':
                return [SimpleNamespace(is_found=False)]

            if name == 'Some Cool Technology':
                return [found('Some Cool Technology', 'prod-2', 'ProductIdentifier')]

            return [SimpleNamespace(is_found=False)]

    class FakeResponse:
        def __init__(self, total):
            self._total = total

        def json(self):
            return {'counts': {'total': self._total}}

    class FakeRFClient:
        def request(self, method, url, params):
            assert method == 'get'
            assert url == 'https://api.recordedfuture.com/v2/vulnerability/search'

            total = {
                'prod-1': 14,
                'prod-2': 3,
            }.get(params['product'], 0)
            return FakeResponse(total)

    monkeypatch.setattr(
        'banshee.lists.list_tech_stack_resolve.EntityMatchMgr', FakeEntityMatchMgr
    )
    monkeypatch.setattr('banshee.lists.list_tech_stack_resolve.RFClient', FakeRFClient)

    result = runner.invoke(
        app,
        args=['tech-stack-resolve', infile.as_posix(), '-o', outfile.as_posix()],
    )
    assert result.exit_code == 0
    assert 'Tech Stack Resolution Summary' in result.output
    assert 'Output file' in result.output
    assert outfile.resolve().as_posix() in ''.join(result.output.split())
    assert 'Technologies supplied' in result.output
    assert 'Technologies found' in result.output
    assert 'Technologies not found' in result.output
    assert '3' in result.output
    assert '2' in result.output
    assert '1' in result.output

    with outfile.open(newline='') as f:
        rows = list(csv.DictReader(f))

    assert rows == [
        {
            'Supplied Input': 'Cisco Nexus 9000 Series',
            'Search Term Used': 'Cisco Nexus 9000 Series',
            'Resolved Entity': 'Cisco Nexus 9000',
            'Type': 'Product',
            'Entity ID': 'prod-1',
            'Mapped CVEs': '14',
        },
        {
            'Supplied Input': 'Some Cool Technology Dude',
            'Search Term Used': 'Some Cool Technology',
            'Resolved Entity': 'Some Cool Technology',
            'Type': 'ProductIdentifier',
            'Entity ID': 'prod-2',
            'Mapped CVEs': '3',
        },
        {
            'Supplied Input': 'No Match Product',
            'Search Term Used': 'N/A',
            'Resolved Entity': 'N/A',
            'Type': 'N/A',
            'Entity ID': 'N/A',
            'Mapped CVEs': '0',
        },
    ]
