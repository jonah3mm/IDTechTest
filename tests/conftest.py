import pytest
from app import create_app, db
from app.models import Asset, Client


@pytest.fixture
def app():
    """Create a fresh application instance with an in-memory database for each test."""
    application = create_app('testing')

    with application.app_context():
        db.create_all()
        _seed_test_data()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def flask_client(app):
    """A test client for the Flask application."""
    return app.test_client()


def _seed_test_data():
    """Insert a minimal set of records for use in tests."""
    client_a = Client(
        name='Acme Corporation',
        contact_email='it@acme.com',
        phone='(555) 000-0001',
    )
    client_b = Client(
        name='Globex Industries',
        contact_email='support@globex.com',
        phone='(555) 000-0002',
    )
    db.session.add_all([client_a, client_b])
    db.session.flush()

    assets = [
        Asset(name='Workstation Alpha', asset_type='workstation', status='active',
              client_id=client_a.id, serial_number='ACM-WS-001'),
        Asset(name='Workstation Beta', asset_type='workstation', status='inactive',
              client_id=client_a.id, serial_number='ACM-WS-002'),
        Asset(name='Primary Server', asset_type='server', status='active',
              client_id=client_a.id, serial_number='ACM-SRV-001'),
        Asset(name='Core Switch', asset_type='network', status='active',
              client_id=client_b.id, serial_number='GLX-NET-001'),
        Asset(name='Label Printer', asset_type='peripheral', status='retired',
              client_id=client_b.id, serial_number='GLX-PRN-001', last_seen=None),
        Asset(name='Dev Laptop', asset_type='workstation', status='active',
              client_id=client_b.id, serial_number='GLX-WS-001'),
        Asset(name='Backup NAS', asset_type='server', status='active',
              client_id=client_b.id, serial_number='GLX-NAS-001'),
        Asset(name='Reception PC', asset_type='workstation', status='inactive',
              client_id=client_a.id, serial_number='ACM-WS-003'),
        Asset(name='Old Firewall', asset_type='network', status='retired',
              client_id=client_a.id, serial_number='ACM-FW-001', last_seen=None),
        Asset(name='Conference Printer', asset_type='peripheral', status='active',
              client_id=client_b.id, serial_number='GLX-PRN-002'),
        Asset(name='Warehouse PC', asset_type='workstation', status='active',
              client_id=client_a.id, serial_number='ACM-WS-004'),
        Asset(name='Edge Router', asset_type='network', status='active',
              client_id=client_b.id, serial_number='GLX-NET-002'),
    ]
    db.session.add_all(assets)
    db.session.commit()
